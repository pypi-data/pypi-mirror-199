#include "bvh.h"

#include <iostream>
#include <numeric>
#include <queue>
#include <sstream>
#include <unordered_set>

#include "../options.h"

using namespace pybind11::literals;

namespace trimesh {

/* -------------- *
 * point_2d_set_t *
 * -------------- */

point_2d_set_t::point_2d_set_t(const std::initializer_list<point_2d_t> &points)
    : points(points) {
    for (size_t i = 0; i < this->points.size(); ++i)
        this->indices[this->points[i]] = i;
}

point_2d_t point_2d_set_t::operator[](size_t i) const { return points[i]; }

size_t point_2d_set_t::add_point(const point_2d_t &p) {
    if (auto it = point_id(p); it.has_value()) return it.value();
    points.push_back(p);
    indices[p] = points.size() - 1;
    return points.size() - 1;
}

size_t point_2d_set_t::size() const { return points.size(); }

size_t point_2d_set_t::get_point(const point_2d_t &p) const {
    return indices.at(p);
}

point_2d_t point_2d_set_t::get_point(size_t i) const { return points[i]; }

std::optional<size_t> point_2d_set_t::point_id(const point_2d_t &p) const {
    if (auto it = indices.find(p); it != indices.end()) return it->second;
    return std::nullopt;
}

const std::vector<point_2d_t> &point_2d_set_t::get_points() const {
    return points;
}

/* ------------------------ *
 * triangle_split_tree_2d_t *
 * ------------------------ */

triangle_split_tree_2d_t::triangle_split_tree_2d_t(
    const face_t &root, const std::vector<point_2d_t> &vertices)
    : root(root) {
    this->faces = {{0, 1, 2}};
    this->children = {{}};
    auto &[a, b, c] = root;
    this->vertices = {vertices[a], vertices[b], vertices[c]};
}

void triangle_split_tree_2d_t::add_triangle(const face_t &f,
                                            const size_t parent) {
    triangle_2d_t t{vertices[f.a], vertices[f.b], vertices[f.c]},
        pt{vertices[faces[parent].a], vertices[faces[parent].b],
           vertices[faces[parent].c]};
    if (t.area() < std::sqrt(get_tolerance())) return;
    if (t.is_clockwise() != pt.is_clockwise()) {
        throw std::runtime_error(
            "Child faces are not oriented the same as the parent face.");
    }

    this->faces.push_back({f.a, f.b, f.c});
    this->children.push_back(std::vector<size_t>{});
    this->children[parent].push_back(this->children.size() - 1);
}

void triangle_split_tree_2d_t::add_triangles(const std::vector<face_t> &fs,
                                             size_t parent) {
    // Checks that parent doesn't have any triangles yet.
    if (!this->children[parent].empty()) {
        std::stringstream ss;
        ss << "Parent face " << get_triangle(parent).to_string()
           << " already has children.";
        throw std::runtime_error(ss.str());
    }

    const auto &parent_face = this->faces[parent];
    const auto parent_triangle = get_triangle(parent);
    const auto parent_area = parent_triangle.area();
    const auto &parent_vertices = parent_triangle.vertices();

    // Checks that all non-shared vertices of the parent face are contained in
    // the child faces.
    for (const auto &f : fs) {
        const auto &child_vertices = get_triangle_from_face(f).vertices();
        for (const auto &v : parent_vertices) {
            if (std::find(child_vertices.begin(), child_vertices.end(), v) ==
                    child_vertices.end() &&
                !v.is_inside_triangle(parent_triangle)) {
                std::stringstream ss;
                ss << "Parent face " << parent_triangle.to_string()
                   << " contains vertex " << v.to_string()
                   << " which is not contained in child face "
                   << get_triangle_from_face(f).to_string() << ".";
                throw std::runtime_error(ss.str());
            }
        }
    }

    // Checks that the signed area of each child equals the signed area of the
    // parent.
    const auto child_area = std::accumulate(
        fs.begin(), fs.end(), 0.0, [&](double area, const face_t &f) {
            return area + get_triangle_from_face(f).area();
        });
    if (std::abs(parent_area - child_area) > std::sqrt(get_tolerance())) {
        std::stringstream ss;
        ss << "Child faces do not have the same area as the parent face. "
           << "Parent area: " << parent_area << ". Child areas:";
        for (const auto &f : fs) {
            ss << " " << get_triangle_from_face(f).area();
        }
        ss << " (sum: " << child_area << ").";
        throw std::runtime_error(ss.str());
    }

    for (auto &f : fs) add_triangle(f, parent);
}

size_t triangle_split_tree_2d_t::add_point(const point_2d_t &p) {
    return this->vertices.add_point(p);
}

bool triangle_split_tree_2d_t::is_leaf(size_t i) const {
    return this->children[i].empty();
}

std::vector<size_t> triangle_split_tree_2d_t::get_leaf_triangles() const {
    std::vector<size_t> leaf_triangles;
    for (size_t i = 0; i < children.size(); i++) {
        if (is_leaf(i)) {
            leaf_triangles.push_back(i);
        }
    }
    return leaf_triangles;
}

std::optional<size_t>
triangle_split_tree_2d_t::get_leaf_triangle_which_contains(
    const point_2d_t &p) const {
    std::queue<size_t> q;
    q.push(0);
    while (!q.empty()) {
        size_t i = q.front();
        q.pop();
        auto t = get_triangle(i);
        if (p.is_inside_triangle(t)) {
            if (is_leaf(i)) {
                return i;
            } else {
                for (auto &child : this->children[i]) {
                    q.push(child);
                }
            }
        }
    }
    return std::nullopt;
}

std::vector<size_t>
triangle_split_tree_2d_t::get_leaf_triangles_which_intersect(
    const line_2d_t &l) const {
    std::unordered_set<size_t> leaf_triangles;
    std::queue<size_t> q;
    q.push(0);
    while (!q.empty()) {
        size_t i = q.front();
        q.pop();
        auto t = get_triangle(i);
        if (l.intersects_triangle(t)) {
            if (is_leaf(i)) {
                leaf_triangles.insert(i);
            } else {
                for (auto &child : this->children[i]) {
                    q.push(child);
                }
            }
        }
    }
    return std::vector<size_t>(leaf_triangles.begin(), leaf_triangles.end());
}

void triangle_split_tree_2d_t::split_triangle(const point_2d_t &p, size_t i) {
    const auto f = faces[i];
    const auto t = get_triangle(i);

    auto intersects_edge = [&](const line_2d_t &l) {
        return l.distance_to_point(p) < get_tolerance();
    };

    std::vector<std::tuple<point_2d_t, point_2d_t, size_t, size_t, size_t>>
        invariants{{t.p1, t.p2, f.a, f.b, f.c},
                   {t.p2, t.p3, f.b, f.c, f.a},
                   {t.p3, t.p1, f.c, f.a, f.b}};

    // Checks if the point is on an edge of the triangle.
    for (auto &[p1, p2, fa, fb, fc] : invariants) {
        if (intersects_edge({p1, p2})) {
            auto new_point = add_point(p);
            add_triangles({{fa, new_point, fc}, {fb, fc, new_point}}, i);
            return;
        }
    }

    // Checks if the point is inside the triangle.
    if (p.is_inside_triangle(t)) {
        auto new_point = add_point(p);
        add_triangles({{f.a, f.b, new_point},
                       {f.b, f.c, new_point},
                       {f.c, f.a, new_point}},
                      i);
        return;
    }

    throw std::runtime_error("Point is outside the triangle.");
}

void triangle_split_tree_2d_t::split_triangle(const line_2d_t &l, size_t i) {
    const auto f = faces[i];
    const auto t = get_triangle(i);

    // Gets the intersection points the line and each edge of the triangle.
    line_2d_t l1{t.p1, t.p2}, l2{t.p2, t.p3}, l3{t.p3, t.p1};
    auto i1 = l1.line_intersection(l), i2 = l2.line_intersection(l),
         i3 = l3.line_intersection(l);

    // Invariant views of the triangle to check.
    std::vector<std::tuple<std::optional<point_2d_t>, std::optional<point_2d_t>,
                           size_t, size_t, size_t>>
        invariants{{i1, i2, f.a, f.b, f.c},
                   {i2, i3, f.b, f.c, f.a},
                   {i3, i1, f.c, f.a, f.b}};

    // Cuts the triangle when it passes through two intersections.
    bool intersects_corner = false;
    for (auto &[ia, ib, fa, fb, fc] : invariants) {
        if (ia.has_value() && ib.has_value()) {
            if (ia.value() == ib.value()) {
                intersects_corner = true;
                continue;
            }

            auto new_point_1 = add_point(ia.value()),
                 new_point_2 = add_point(ib.value());
            add_triangles({{fa, new_point_1, new_point_2},
                           {new_point_1, fb, new_point_2},
                           {new_point_2, fc, fa}},
                          i);
            return;
        }
    }

    // Lines which just intersect at a corner are ignored.
    if (intersects_corner) return;

    bool p1_in_t = t.contains_point(l.p1), p2_in_t = t.contains_point(l.p2);

    // Cuts the triangle when it passes through a single intersection.
    for (auto &[ia, ib, fa, fb, fc] : invariants) {
        if (ia.has_value()) {
            // Checks that at least one of the points is inside or on an edge.
            if (!p1_in_t && !p2_in_t)
                throw std::runtime_error("Unexpected intersection");

            // Chooses an inside and outside point (although the outside point
            // may actually be the intersection point).
            std::optional<point_2d_t> p_in = std::nullopt;
            if (p1_in_t && l.p1 != ia.value())
                p_in = l.p1;
            else if (p2_in_t && l.p2 != ia.value())
                p_in = l.p2;

            if (!p_in.has_value()) {
                auto fi = add_point(ia.value());
                add_triangles({{fa, fi, fc}, {fb, fc, fi}}, i);
            } else {
                auto fi = add_point(ia.value());
                auto fp = add_point(p_in.value());
                add_triangles(
                    {{fa, fi, fp}, {fa, fp, fc}, {fb, fp, fi}, {fb, fc, fp}},
                    i);
            }

            return;
        }
    }

    // Cuts the triangle when both points are entirely inside.
    if (p1_in_t && p2_in_t) {
        auto new_point_1 = add_point(l.p1), new_point_2 = add_point(l.p2);
        line_2d_t l_p1_b{l.p1, this->vertices[f.b]},
            l_p2_c{l.p2, this->vertices[f.c]};
        if (l_p1_b.line_intersection(l_p2_c).has_value()) {
            add_triangles({{f.a, new_point_1, new_point_2},
                           {f.a, new_point_1, f.c},
                           {f.a, new_point_2, f.b}},
                          i);
        } else {
            add_triangles({{f.a, new_point_1, new_point_2},
                           {f.a, new_point_1, f.b},
                           {f.a, new_point_2, f.c}},
                          i);
        }
        return;
    }

    // Throw an error because we should only be considering splitting
    // for lines which intersect a triangle.
    throw std::runtime_error("Triangle split failed.");
}

const face_t &triangle_split_tree_2d_t::get_face(size_t i) const {
    return this->faces[i];
}

triangle_2d_t triangle_split_tree_2d_t::get_triangle(size_t i) const {
    return get_triangle_from_face(this->faces[i]);
}

triangle_2d_t triangle_split_tree_2d_t::get_triangle_from_face(
    const face_t &f) const {
    const auto &[p1, p2, p3] = f;
    const auto v1 = this->vertices[p1], v2 = this->vertices[p2],
               v3 = this->vertices[p3];
    triangle_2d_t ret_val{v1, v2, v3};
    return ret_val;
}

const std::vector<size_t> triangle_split_tree_2d_t::get_children(
    size_t i) const {
    return children[i];
}

const std::vector<face_t> triangle_split_tree_2d_t::get_leaf_faces(
    size_t offset) const {
    auto get_vertex = [&](const size_t v) {
        switch (v) {
            case 0:
                return this->root.a;
            case 1:
                return this->root.b;
            case 2:
                return this->root.c;
            default:
                return v - 3 + offset;
        }
    };
    std::vector<face_t> leaf_faces;
    for (size_t i = 0; i < faces.size(); i++) {
        if (is_leaf(i)) {
            auto &[a, b, c] = faces[i];
            leaf_faces.push_back({get_vertex(a), get_vertex(b), get_vertex(c)});
        }
    }
    return leaf_faces;
}

const std::vector<point_2d_t> triangle_split_tree_2d_t::get_vertices() const {
    auto &points = this->vertices.get_points();
    std::vector<point_2d_t> v(points.begin() + 3, points.end());
    return v;
}

const size_t triangle_split_tree_2d_t::count_leaf_triangles() const {
    size_t count = 0;
    for (size_t i = 0; i < faces.size(); i++) {
        if (is_leaf(i)) {
            count++;
        }
    }
    return count;
}

/* ------------------------ *
 * delaunay_split_tree_2d_t *
 * ------------------------ */

void delaunay_split_tree_2d_t::make_delaunay(const size_t &pi, const edge_t &e,
                                             const size_t &ti) {
    const auto e_rev = e.flip();

    if (this->edge_to_face.find(e_rev) == this->edge_to_face.end()) {
        return;
    }

    size_t tj = this->edge_to_face[e_rev];
    const auto &tj_face = this->faces[tj];
    const auto &tj_tri = this->get_triangle(tj_face);

    if (tj_tri.circumcircle_contains(this->vertices[pi], -get_tolerance())) {
        const auto &pj = tj_face.get_other_vertex(e_rev);
        const auto tk = this->add_triangle({pi, pj, e.b}, {ti, tj}),
                   tl = this->add_triangle({pj, pi, e.a}, {ti, tj});

        this->make_delaunay(pi, {e.a, pj, true}, tl);
        this->make_delaunay(pi, {pj, e.b, true}, tk);
    }
}

size_t delaunay_split_tree_2d_t::add_triangle(
    const face_t &f, const std::vector<size_t> &parents) {
    const size_t i = this->faces.size();
    for (const auto &parent : parents) {
        this->children[parent].push_back(i);
    }
    this->faces.push_back(f);
    for (const auto &edge : f.get_edges(true)) {
        this->edge_to_face[edge] = i;
    }
    this->children.push_back({});
    return i;
}

delaunay_split_tree_2d_t::delaunay_split_tree_2d_t(const triangle_2d_t &root)
    : root(root) {
    this->faces = {{0, 1, 2}};
    for (const auto &edge : this->faces[0].get_edges(true))
        this->edge_to_face[edge] = 0;
    this->children = {{}};
    this->vertices = {root.p1, root.p2, root.p3};
}

bool delaunay_split_tree_2d_t::is_leaf(size_t i) const {
    return this->children[i].empty();
}

size_t delaunay_split_tree_2d_t::find_leaf_index(const point_2d_t &p) const {
    size_t i = 0;
    while (!is_leaf(i)) {
        // Gets the closest triangle to the point.
        double min_dist = std::numeric_limits<double>::max();
        size_t min_index = 0;
        for (const auto &child_id : this->children[i]) {
            const auto &child = this->faces[child_id];
            const triangle_2d_t t{this->vertices[child.a],
                                  this->vertices[child.b],
                                  this->vertices[child.c]};
            double t_dist = p.distance_to_triangle(t);
            if (t_dist < min_dist) {
                min_dist = t_dist;
                min_index = child_id;
            }
        }

        if (min_dist > get_tolerance()) {
            std::ostringstream ss;
            ss << "Could not find leaf triangle for point " << p.to_string()
               << " in triangle " << this->get_triangle(i).to_string()
               << " with " << this->children[i].size()
               << " children:" << std::endl;
            for (const auto &child_id : this->children[i]) {
                ss << " - " << this->get_triangle(child_id).to_string()
                   << " (dist: "
                   << p.distance_to_triangle(this->get_triangle(child_id))
                   << ")" << std::endl;
            }
            throw std::runtime_error(ss.str());
        }

        i = min_index;
    }
    return i;
}

const face_t &delaunay_split_tree_2d_t::get_face(size_t i) const {
    return this->faces[i];
}

triangle_2d_t delaunay_split_tree_2d_t::get_triangle(const face_t &f) const {
    return triangle_2d_t{this->vertices[f.a], this->vertices[f.b],
                         this->vertices[f.c]};
}

triangle_2d_t delaunay_split_tree_2d_t::get_triangle(size_t i) const {
    const auto &f = this->get_face(i);
    return this->get_triangle(f);
}

std::vector<size_t> delaunay_split_tree_2d_t::get_leaf_triangles() const {
    std::vector<size_t> leaf_triangles;
    for (size_t i = 0; i < this->faces.size(); i++) {
        if (is_leaf(i)) {
            leaf_triangles.push_back(i);
        }
    }
    return leaf_triangles;
}

void delaunay_split_tree_2d_t::split_triangle(const point_2d_t &p, size_t i,
                                              bool make_delaunay) {
    // if (!this->get_triangle(i).contains_point(p)) {
    //     std::ostringstream ss;
    //     ss << "Point " << p.to_string() << " is not in triangle "
    //        << this->get_triangle(i).to_string();
    //     throw std::runtime_error(ss.str());
    // }

    const auto [fa, fb, fc] = this->faces[i];
    const auto &va = this->vertices[fa], &vb = this->vertices[fb],
               &vc = this->vertices[fc];
    if (p == va || p == vb || p == vc) return;
    const auto pi = this->vertices.add_point(p);

    // Checks if the point intersects an edge.
    for (const auto [ea, eb, directed] : this->faces[i].get_edges(true)) {
        const auto &v1 = this->vertices[ea], &v2 = this->vertices[eb];
        const line_2d_t l{v1, v2};
        if (l.closest_point(p) == p) {
            const edge_t e{ea, eb, directed}, e_rev{eb, ea, directed};
            const size_t j = this->edge_to_face[e_rev];
            const size_t pc = this->faces[i].get_other_vertex(e),
                         pn = this->faces[j].get_other_vertex(e_rev);

            // Splits each triangle.
            const auto t1 = this->add_triangle({pi, pc, ea}, {i}),
                       t2 = this->add_triangle({pi, eb, pc}, {i}),
                       t3 = this->add_triangle({pi, ea, pn}, {j}),
                       t4 = this->add_triangle({pi, pn, eb}, {j});

            // Makes the new triangles Delaunay.
            if (make_delaunay) {
                this->make_delaunay(pi, {pc, ea, true}, t1);
                this->make_delaunay(pi, {eb, pc, true}, t2);
                this->make_delaunay(pi, {ea, pn, true}, t3);
                this->make_delaunay(pi, {pn, eb, true}, t4);
            }

            return;
        }
    }

    // Splits the current triangle.
    const auto t1 = this->add_triangle({fa, fb, pi}, {i});
    const auto t2 = this->add_triangle({fb, fc, pi}, {i});
    const auto t3 = this->add_triangle({fc, fa, pi}, {i});

    // Makes the new triangles Delaunay.
    if (make_delaunay) {
        this->make_delaunay(pi, {fa, fb, true}, t1);
        this->make_delaunay(pi, {fb, fc, true}, t2);
        this->make_delaunay(pi, {fc, fa, true}, t3);
    }
}

const point_2d_set_t &delaunay_split_tree_2d_t::get_vertices() const {
    return this->vertices;
}

/* -------- *
 * bvh_2d_t *
 * -------- */

void sort_bounding_boxes_for_bvh(const std::vector<bounding_box_2d_t> &boxes,
                                 std::vector<size_t> &indices, bvh_tree_t &tree,
                                 size_t lo, size_t hi) {
    if (hi - lo < 2) {
        tree[lo] = {indices[lo], -1, -1, boxes[indices[lo]]};
        return;
    }

    double min_x = std::numeric_limits<double>::max(),
           min_y = std::numeric_limits<double>::max(),
           max_x = std::numeric_limits<double>::lowest(),
           max_y = std::numeric_limits<double>::lowest();
    for (size_t i = lo; i < hi; i++) {
        const auto &box = boxes[indices[i]];
        min_x = std::min(min_x, box.min.x);
        min_y = std::min(min_y, box.min.y);
        max_x = std::max(max_x, box.max.x);
        max_y = std::max(max_y, box.max.y);
    }

    double dx = max_x - min_x, dy = max_y - min_y;
    size_t axis = 0;
    if (dx < dy) axis = 1;

    auto get_axis_vals = [&axis](const bounding_box_2d_t &box) {
        auto min = box.min, max = box.max;
        switch (axis) {
            case 0:
                return std::make_pair(min.x, max.x);
            case 1:
                return std::make_pair(min.y, max.y);
            default:
                throw std::runtime_error("Invalid axis.");
        }
    };

    auto get_sort_val = [&boxes, &get_axis_vals](size_t i) {
        auto [min, max] = get_axis_vals(boxes[i]);
        return (min + max) / 2;
    };

    std::sort(indices.begin() + lo, indices.begin() + hi,
              [&get_sort_val](const size_t &a, const size_t &b) {
                  return get_sort_val(a) < get_sort_val(b);
              });

    size_t mid = (hi - lo + 1) / 2;
    std::swap(indices[lo], indices[lo + mid]);
    tree[lo] = {indices[lo],
                mid == 1 ? -1 : (int)(lo + 1),
                mid == (hi - lo) ? -1 : (int)(lo + mid),
                {{min_x, min_y}, {max_x, max_y}}};

    sort_bounding_boxes_for_bvh(boxes, indices, tree, lo + 1, lo + mid);
    sort_bounding_boxes_for_bvh(boxes, indices, tree, lo + mid, hi);
}

bvh_2d_t::bvh_2d_t(const trimesh_2d_t &t) : bvh_2d_t(t.faces(), t.vertices()) {}

bvh_2d_t::bvh_2d_t(const face_list_t &faces,
                   const std::vector<point_2d_t> &vertices)
    : faces(faces), vertices(vertices) {
    std::vector<bounding_box_2d_t> boxes;
    for (const auto &face : faces)
        boxes.push_back(bounding_box_2d_t({triangle_2d_t(
            {vertices[face.a], vertices[face.b], vertices[face.c]})}));

    std::vector<size_t> indices(boxes.size());
    std::iota(indices.begin(), indices.end(), 0);
    tree.resize(boxes.size());
    sort_bounding_boxes_for_bvh(boxes, indices, tree, 0, boxes.size());
}

void line_intersections_helper(const bvh_tree_t tree, const face_list_t &faces,
                               const std::vector<point_2d_t> &vertices, int id,
                               const line_2d_t &l, std::vector<face_t> &intrs,
                               const std::optional<size_t> max_intersections) {
    if (id < 0 || id >= tree.size()) throw std::runtime_error("Invalid ID");

    auto &[face_id, lhs, rhs, box] = tree[id];

    // If the triangle doesn't intersect the current bounding box, then
    // there's no need to check child triangles.
    if (!l.intersects_bounding_box(box)) {
        return;
    }

    // Checks if the line intersects the current triangle.
    auto &face_indices = faces[face_id];
    triangle_2d_t face = {vertices[face_indices.a], vertices[face_indices.b],
                          vertices[face_indices.c]};
    if (l.intersects_triangle(face)) {
        intrs.push_back(face_indices);
    }
    if (max_intersections && intrs.size() >= *max_intersections) return;

    // Recursively checks the left and right subtrees.
    if (lhs != -1)
        line_intersections_helper(tree, faces, vertices, lhs, l, intrs,
                                  max_intersections);
    if (max_intersections && intrs.size() >= *max_intersections) return;
    if (rhs != -1)
        line_intersections_helper(tree, faces, vertices, rhs, l, intrs,
                                  max_intersections);
}

std::vector<face_t> bvh_2d_t::line_intersections(
    const line_2d_t &l, const std::optional<size_t> max_intersections) const {
    std::vector<face_t> intrs;
    line_intersections_helper(tree, faces, vertices, 0, l, intrs,
                              max_intersections);
    return intrs;
}

void triangle_intersections_helper(
    const bvh_tree_t tree, const face_list_t &faces,
    const std::vector<point_2d_t> &vertices, int id, const triangle_2d_t &t,
    std::vector<face_t> &intrs, const std::optional<size_t> max_intersections) {
    if (id < 0 || id >= tree.size()) throw std::runtime_error("Invalid ID");

    auto &[face_id, lhs, rhs, box] = tree[id];

    // If the triangle doesn't intersect the current bounding box, then
    // there's no need to check child triangles.
    if (!t.intersects_bounding_box(box)) {
        return;
    }

    // Checks if the line intersects the current triangle.
    auto &face_indices = faces[face_id];
    triangle_2d_t face = {vertices[face_indices.a], vertices[face_indices.b],
                          vertices[face_indices.c]};
    if (t.intersects_triangle(face)) {
        intrs.push_back(face_indices);
    }
    if (max_intersections && intrs.size() >= *max_intersections) return;

    // Recursively checks the left and right subtrees.
    if (lhs != -1)
        triangle_intersections_helper(tree, faces, vertices, lhs, t, intrs,
                                      max_intersections);
    if (max_intersections && intrs.size() >= *max_intersections) return;
    if (rhs != -1)
        triangle_intersections_helper(tree, faces, vertices, rhs, t, intrs,
                                      max_intersections);
}

std::vector<face_t> bvh_2d_t::triangle_intersections(
    const triangle_2d_t &l,
    const std::optional<size_t> max_intersections) const {
    std::vector<face_t> intrs;
    triangle_intersections_helper(tree, faces, vertices, 0, l, intrs,
                                  max_intersections);
    return intrs;
}

std::optional<face_t> get_containing_face_helper(
    const bvh_tree_t tree, const face_list_t &faces,
    const std::vector<point_2d_t> &vertices, int id, const triangle_2d_t &t) {
    if (id < 0 || id >= tree.size()) return std::nullopt;

    auto &[face_id, lhs, rhs, box] = tree[id];

    // If some part of the triangle is outside the current bounding box,
    // then the triangle is not inside the mesh.
    if (!box.contains_triangle(t)) {
        return std::nullopt;
    }

    // Checks if the triangle is inside the current triangle.
    auto &face_indices = faces[face_id];
    triangle_2d_t face = {vertices[face_indices.a], vertices[face_indices.b],
                          vertices[face_indices.c]};
    if (face.contains_triangle(t)) {
        return face_indices;
    }

    // Recursively checks the left and right subtrees.
    if (auto face = get_containing_face_helper(tree, faces, vertices, lhs, t))
        return face;
    if (auto face = get_containing_face_helper(tree, faces, vertices, rhs, t))
        return face;
    return std::nullopt;
}

std::optional<face_t> bvh_2d_t::get_containing_face(
    const triangle_2d_t &t) const {
    return get_containing_face_helper(tree, faces, vertices, 0, t);
}

std::string bvh_2d_t::to_string() const {
    std::stringstream ss;
    ss << "BVH(";
    ss << "faces = " << faces.size() << ", ";
    ss << "vertices = " << vertices.size() << ", ";
    ss << "tree = " << tree.size() << ")";
    return ss.str();
}

void add_2d_bvh_modules(py::module &m) {
    auto ttree_2d =
        py::class_<triangle_split_tree_2d_t>(m, "TriangleSplitTree2D");
    auto dtree_2d =
        py::class_<delaunay_split_tree_2d_t>(m, "DelaunaySplitTree2D");
    auto bvh_2d = py::class_<bvh_2d_t>(m, "BVH2D");

    ttree_2d
        .def(py::init<const face_t &, const std::vector<point_2d_t> &>(),
             "face"_a, "vertices"_a,
             "Constructs a 2D triangle split tree from a face and a list "
             "of vertices.")
        .def("is_leaf", &triangle_split_tree_2d_t::is_leaf, "i"_a,
             "Returns true if the node is a leaf.")
        .def("get_leaf_triangles_which_intersect",
             &triangle_split_tree_2d_t::get_leaf_triangles_which_intersect,
             "line"_a, "Returns the triangles which intersect the line.")
        .def("split_triangle",
             py::overload_cast<const point_2d_t &, size_t>(
                 &triangle_split_tree_2d_t::split_triangle),
             "point"_a, "i"_a, "Splits a triangle at a point.")
        .def("split_triangle",
             py::overload_cast<const line_2d_t &, size_t>(
                 &triangle_split_tree_2d_t::split_triangle),
             "line"_a, "i"_a, "Splits a triangle at a line.")
        .def("get_triangle", &triangle_split_tree_2d_t::get_triangle, "i"_a,
             "Returns the triangle associated with the node.")
        .def("get_children", &triangle_split_tree_2d_t::get_children, "i"_a,
             "Returns the children of a node")
        .def("get_vertices", &triangle_split_tree_2d_t::get_vertices,
             "Returns the vertices of the tree.")
        .def("__len__", &triangle_split_tree_2d_t::count_leaf_triangles,
             "Returns the number of leaf triangles", py::is_operator())
        .def("__getitem__", &triangle_split_tree_2d_t::get_triangle, "i"_a,
             "Get a node", py::is_operator());

    dtree_2d
        .def(py::init<const triangle_2d_t &>(), "root"_a,
             "Constructs a 2D Delaunay split tree from a triangle.")
        .def("is_leaf", &delaunay_split_tree_2d_t::is_leaf, "i"_a,
             "Returns true if the node is a leaf.")
        .def("get_leaf_triangles",
             &delaunay_split_tree_2d_t::get_leaf_triangles,
             "Returns the triangles associated with a leaf.")
        .def("split_triangle", &delaunay_split_tree_2d_t::split_triangle,
             "point"_a, "i"_a, "make_delaunay"_a = false,
             "Splits a triangle at a point.");

    bvh_2d
        .def(py::init<const trimesh_2d_t &>(), "Boundary volume hierarchy",
             "trimesh"_a)
        .def(py::init<const face_list_t &, const std::vector<point_2d_t> &>(),
             "Boundary volume hierarchy", "faces"_a, "vertices"_a)
        .def("__str__", &bvh_2d_t::to_string, py::is_operator())
        .def("__repr__", &bvh_2d_t::to_string, py::is_operator())
        .def("line_intersections", &bvh_2d_t::line_intersections,
             "Intersections", "triangle"_a,
             "max_intersections"_a = std::nullopt)
        .def("triangle_intersections", &bvh_2d_t::triangle_intersections,
             "Intersections", "triangle"_a,
             "max_intersections"_a = std::nullopt)
        .def_property_readonly("faces", &bvh_2d_t::get_faces, "Faces")
        .def_property_readonly("vertices", &bvh_2d_t::get_vertices, "Vertices")
        .def_property_readonly("tree", &bvh_2d_t::get_tree, "Tree");
}

}  // namespace trimesh
