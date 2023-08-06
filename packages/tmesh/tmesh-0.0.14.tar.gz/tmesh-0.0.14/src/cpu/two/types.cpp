#include "types.h"

#include <algorithm>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <sstream>
#include <stack>
#include <unordered_map>
#include <unordered_set>

#include "../options.h"
#include "boolean.h"
#include "bvh.h"

using namespace pybind11::literals;

namespace trimesh {

/* ---------- *
 * point_2d_t *
 * ---------- */

point_2d_t point_2d_t::operator+=(const point_2d_t &p) {
    x += p.x;
    y += p.y;
    return *this;
}

point_2d_t point_2d_t::operator-=(const point_2d_t &p) {
    x -= p.x;
    y -= p.y;
    return *this;
}

point_2d_t point_2d_t::operator*=(const point_2d_t &p) {
    x *= p.x;
    y *= p.y;
    return *this;
}

point_2d_t point_2d_t::operator*=(double s) {
    x *= s;
    y *= s;
    return *this;
}

point_2d_t point_2d_t::operator/=(const point_2d_t &p) {
    x /= p.x;
    y /= p.y;
    return *this;
}

point_2d_t point_2d_t::operator/=(double s) {
    x /= s;
    y /= s;
    return *this;
}

bool point_2d_t::operator==(const point_2d_t &p) const {
    return distance_to_point(p) < get_tolerance();
}

bool point_2d_t::operator!=(const point_2d_t &p) const { return !(*this == p); }

bool point_2d_t::operator<(const point_2d_t &p) const {
    if (*this == p) return false;
    if (x < p.x - get_tolerance()) return true;
    if (x > p.x + get_tolerance()) return false;
    return y < p.y - get_tolerance();
}

point_2d_t point_2d_t::operator<<=(const affine_2d_t &a) {
    point_2d_t p = *this << a;
    x = p.x;
    y = p.y;
    return *this;
}

point_2d_t point_2d_t::normalize() const {
    double l = length();
    return point_2d_t{x / l, y / l};
}

point_2d_t point_2d_t::rotate(double angle) const {
    double c = std::cos(angle);
    double s = std::sin(angle);
    return point_2d_t{x * c - y * s, x * s + y * c};
}

point_2d_t point_2d_t::perpendicular() const { return {-y, x}; }

double point_2d_t::determinant(const point_2d_t &other) const {
    return x * other.y - y * other.x;
}

double point_2d_t::length() const { return std::sqrt(x * x + y * y); }

double point_2d_t::dot(const point_2d_t &other) const {
    return x * other.x + y * other.y;
}

double point_2d_t::cross(const point_2d_t &other) const {
    return x * other.y - y * other.x;
}

double point_2d_t::angle(const point_2d_t &other) const {
    double dot = this->dot(other);
    double det = this->determinant(other);
    return std::atan2(det, dot);
}

barycentric_coordinates_t point_2d_t::barycentric_coordinates(
    const triangle_2d_t &t) const {
    point_2d_t v0 = t.p2 - t.p1;
    point_2d_t v1 = t.p3 - t.p1;
    point_2d_t v2 = *this - t.p1;

    double d00 = v0.dot(v0);
    double d01 = v0.dot(v1);
    double d11 = v1.dot(v1);
    double d20 = v2.dot(v0);
    double d21 = v2.dot(v1);
    double denom = d00 * d11 - d01 * d01;

    double v = (d11 * d20 - d01 * d21) / denom;
    double w = (d00 * d21 - d01 * d20) / denom;
    double u = 1.0 - v - w;

    return {u, v, w};
}

bool point_2d_t::is_inside_triangle(const triangle_2d_t &t) const {
    barycentric_coordinates_t bary = barycentric_coordinates(t);
    return bary.u >= -get_tolerance() && bary.v >= -get_tolerance() &&
           bary.w >= -get_tolerance();
}

bool point_2d_t::is_inside_bounding_box(const bounding_box_2d_t &bb) const {
    return x >= bb.min.x && x <= bb.max.x && y >= bb.min.y && y <= bb.max.y;
}

double point_2d_t::distance_to_point(const point_2d_t &p) const {
    return (*this - p).length();
}

double point_2d_t::distance_to_line(const line_2d_t &l) const {
    return l.distance_to_point(*this);
}

double point_2d_t::distance_to_triangle(const triangle_2d_t &t) const {
    return t.distance_to_point(*this);
}

double point_2d_t::distance_to_bounding_box(const bounding_box_2d_t &bb) const {
    return bb.distance_to_point(*this);
}

std::optional<point_2d_t> point_2d_t::project_to_line(
    const line_2d_t &l) const {
    double dx = l.p2.x - l.p1.x, dy = l.p2.y - l.p1.y;
    double t = ((x - l.p1.x) * dx + (y - l.p1.y) * dy) / (dx * dx + dy * dy);
    if (t < 0.0 || t > 1.0) return std::nullopt;
    return point_2d_t{l.p1.x + t * dx, l.p1.y + t * dy};
}

std::string point_2d_t::to_string() const {
    std::ostringstream ss;
    ss << "Point2D(" << x << ", " << y << ")";
    return ss.str();
}

size_t point_2d_hash_fn(const point_2d_t &p) {
    auto hf = std::hash<double>();
    return hf(p.x) ^ hf(p.y);
}

size_t __point_2d_hash_fn::operator()(const point_2d_t &p) const {
    return point_2d_hash_fn(p);
}

point_2d_t operator+(const point_2d_t &p1, const point_2d_t &p2) {
    return {p1.x + p2.x, p1.y + p2.y};
}

point_2d_t operator-(const point_2d_t &p1, const point_2d_t &p2) {
    return {p1.x - p2.x, p1.y - p2.y};
}

point_2d_t operator*(const point_2d_t &p1, const point_2d_t &p2) {
    return {p1.x * p2.x, p1.y * p2.y};
}

point_2d_t operator*(const point_2d_t &p, double s) {
    return {p.x * s, p.y * s};
}

point_2d_t operator*(double s, const point_2d_t &p) {
    return {p.x * s, p.y * s};
}

point_2d_t operator/(const point_2d_t &p1, const point_2d_t &p2) {
    return {p1.x / p2.x, p1.y / p2.y};
}

point_2d_t operator/(const point_2d_t &p, double s) {
    return {p.x / s, p.y / s};
}

bool is_convex(const point_2d_t &a, const point_2d_t &b, const point_2d_t &c) {
    // Equivalent to angle(a, b, c) <= 0, meaning that a convex polygon
    // is traversed in a counter-clockwise direction.
    return (b - a).determinant(c - a) >= 0;
}

/* --------- *
 * line_2d_t *
 * --------- */

bool line_2d_t::operator==(const line_2d_t &other) const {
    return p1 == other.p1 && p2 == other.p2;
}

bool line_2d_t::operator!=(const line_2d_t &other) const {
    return !(*this == other);
}

bool line_2d_t::operator<(const line_2d_t &other) const {
    return *this != other && (p1 < other.p1 || p2 < other.p2);
}

line_2d_t line_2d_t::operator<<=(const affine_2d_t &a) {
    p1 <<= a;
    p2 <<= a;
    return *this;
}

point_2d_t line_2d_t::closest_point(const point_2d_t &p) const {
    point_2d_t v = p2 - p1;
    point_2d_t w = p - p1;

    double c1 = w.dot(v);
    if (c1 <= 0.0) return p1;

    double c2 = v.dot(v);
    if (c2 <= c1) return p2;

    double b = c1 / c2;
    return p1 + v * b;
}

std::optional<point_2d_t> line_2d_t::line_intersection(
    const line_2d_t &l) const {
    point_2d_t r = p2 - p1;
    point_2d_t s = l.p2 - l.p1;

    double rxs = r.cross(s);
    if (std::abs(rxs) < get_tolerance()) return std::nullopt;

    point_2d_t qmp1 = l.p1 - p1;
    double t = qmp1.cross(s) / rxs;
    double u = qmp1.cross(r) / rxs;

    if (t < -get_tolerance() || t > 1.0 + get_tolerance() ||
        u < -get_tolerance() || u > 1.0 + get_tolerance())
        return std::nullopt;

    return p1 + r * t;
}

bool line_2d_t::intersects_triangle(const triangle_2d_t &t) const {
    if (p1.is_inside_triangle(t) || p2.is_inside_triangle(t)) {
        return true;
    }
    for (auto &l : t.edges()) {
        if (line_intersection(l)) return true;
    }
    return false;
}

std::vector<point_2d_t> line_2d_t::triangle_intersection(
    const triangle_2d_t &t) const {
    std::vector<point_2d_t> points;
    if (p1.is_inside_triangle(t)) points.push_back(p1);
    if (p2.is_inside_triangle(t)) points.push_back(p2);
    for (auto &l : t.edges()) {
        std::optional<point_2d_t> p = line_intersection(l);
        if (p) points.push_back(*p);
    }
    return points;
}

bool line_2d_t::intersects_bounding_box(const bounding_box_2d_t &b) const {
    if (p1.is_inside_bounding_box(b) || p2.is_inside_bounding_box(b)) {
        return true;
    }
    for (auto &l : b.edges()) {
        if (line_intersection(l)) return true;
    }
    return false;
}

double line_2d_t::distance_to_point(const point_2d_t &p) const {
    point_2d_t pb = closest_point(p);
    return p.distance_to_point(pb);
}

double line_2d_t::distance_to_line(const line_2d_t &l) const {
    std::optional<point_2d_t> p = line_intersection(l);

    if (p) return 0.0;

    return std::min({distance_to_point(l.p1), distance_to_point(l.p2),
                     l.distance_to_point(p1), l.distance_to_point(p2)});
}

double line_2d_t::distance_to_triangle(const triangle_2d_t &t) const {
    return t.distance_to_line(*this);
}

double line_2d_t::distance_to_bounding_box(const bounding_box_2d_t &bb) const {
    return bb.distance_to_line(*this);
}

std::string line_2d_t::to_string() const {
    std::ostringstream ss;
    ss << "Line2D(" << p1.to_string() << ", " << p2.to_string() << ")";
    return ss.str();
}

/* ------------- *
 * triangle_2d_t *
 * ------------- */

bool triangle_2d_t::operator==(const triangle_2d_t &other) const {
    return (p1 == other.p1 && p2 == other.p2 && p3 == other.p3) ||
           (p1 == other.p2 && p2 == other.p3 && p3 == other.p1) ||
           (p1 == other.p3 && p2 == other.p1 && p3 == other.p2);
}

bool triangle_2d_t::operator!=(const triangle_2d_t &other) const {
    return !(*this == other);
}

bool triangle_2d_t::operator<(const triangle_2d_t &other) const {
    if (*this == other) return false;

    // Sorts triangles.
    auto [p1, p2, p3] = *this;
    auto [q1, q2, q3] = other;
    if (p1 < p2) std::swap(p1, p2);
    if (p1 < p3) std::swap(p1, p3);
    if (p2 < p3) std::swap(p2, p3);
    if (q1 < q2) std::swap(q1, q2);
    if (q1 < q3) std::swap(q1, q3);
    if (q2 < q3) std::swap(q2, q3);
    return p1 < q1 || p2 < q2 || p3 < q3;
}

triangle_2d_t triangle_2d_t::operator<<=(const affine_2d_t &a) {
    p1 <<= a;
    p2 <<= a;
    p3 <<= a;
    return *this;
}

double triangle_2d_t::area() const {
    return std::abs((p1.x - p3.x) * (p2.y - p1.y) -
                    (p1.x - p2.x) * (p3.y - p1.y)) /
           2.0;
}

point_2d_t triangle_2d_t::center() const { return (p1 + p2 + p3) / 3.0; }

std::vector<point_2d_t> triangle_2d_t::vertices() const { return {p1, p2, p3}; }

std::vector<line_2d_t> triangle_2d_t::edges() const {
    return {{p1, p2}, {p2, p3}, {p3, p1}};
}

bool triangle_2d_t::is_clockwise() const {
    return (p3 - p1).cross(p2 - p1) < 0.0;
}

circle_2d_t triangle_2d_t::circumcircle() const { return {*this}; }

bool triangle_2d_t::circumcircle_contains(const point_2d_t &p,
                                          double tolerance) const {
    // Naive version.
    // return circumcircle().contains_point(p, tolerance);

    // Faster version.
    double x0 = p1.x - p.x;
    double y0 = p1.y - p.y;
    double x1 = p2.x - p.x;
    double y1 = p2.y - p.y;
    double x2 = p3.x - p.x;
    double y2 = p3.y - p.y;

    double z0 = x0 * (p1.x + p.x) + y0 * (p1.y + p.y);
    double z1 = x1 * (p2.x + p.x) + y1 * (p2.y + p.y);
    double z2 = x2 * (p3.x + p.x) + y2 * (p3.y + p.y);

    // Determinant of
    // | x0 y0 z0 |
    // | x1 y1 z1 |
    // | x2 y2 z2 |
    double det = x0 * (y1 * z2 - y2 * z1) - y0 * (x1 * z2 - x2 * z1) +
                 z0 * (x1 * y2 - x2 * y1);

    return det > -tolerance;
}

bool triangle_2d_t::contains_point(const point_2d_t &p) const {
    return p.is_inside_triangle(*this);
}

bool triangle_2d_t::contains_triangle(const triangle_2d_t &t) const {
    return t.p1.is_inside_triangle(*this) && t.p2.is_inside_triangle(*this) &&
           t.p3.is_inside_triangle(*this);
}

bool triangle_2d_t::intersects_bounding_box(const bounding_box_2d_t &bb) const {
    return bb.intersects_triangle(*this);
}

bool triangle_2d_t::intersects_triangle(const triangle_2d_t &t) const {
    if (t.contains_point(p1) || t.contains_point(p2) || t.contains_point(p3))
        return true;
    if (contains_point(t.p1) || contains_point(t.p2) || contains_point(t.p3))
        return true;
    for (auto &l : edges()) {
        if (l.intersects_triangle(t)) return true;
    }
    return false;
}

std::vector<point_2d_t> triangle_2d_t::triangle_intersection(
    const triangle_2d_t &t) const {
    std::vector<point_2d_t> points;
    for (auto &l : edges()) {
        std::vector<point_2d_t> p = l.triangle_intersection(t);
        points.insert(points.end(), p.begin(), p.end());
    }
    return points;
}

double triangle_2d_t::distance_to_point(const point_2d_t &p) const {
    if (p.is_inside_triangle(*this)) return 0.0;
    line_2d_t l1 = {p1, p2}, l2 = {p2, p3}, l3 = {p3, p1};
    return std::min({l1.distance_to_point(p), l2.distance_to_point(p),
                     l3.distance_to_point(p)});
}

double triangle_2d_t::distance_to_line(const line_2d_t &l) const {
    if (l.p1.is_inside_triangle(*this) || l.p2.is_inside_triangle(*this))
        return 0.0;
    line_2d_t l1 = {p1, p2}, l2 = {p2, p3}, l3 = {p3, p1};
    return std::min({l1.distance_to_line(l), l2.distance_to_line(l),
                     l3.distance_to_line(l)});
}

double triangle_2d_t::distance_to_triangle(const triangle_2d_t &t) const {
    line_2d_t l1 = {p1, p2}, l2 = {p2, p3}, l3 = {p3, p1};
    line_2d_t l4 = {t.p1, t.p2}, l5 = {t.p2, t.p3}, l6 = {t.p3, t.p1};
    return std::min({l1.distance_to_line(l4), l1.distance_to_line(l5),
                     l1.distance_to_line(l6), l2.distance_to_line(l4),
                     l2.distance_to_line(l5), l2.distance_to_line(l6),
                     l3.distance_to_line(l4), l3.distance_to_line(l5),
                     l3.distance_to_line(l6)});
}

double triangle_2d_t::distance_to_bounding_box(
    const bounding_box_2d_t &b) const {
    return b.distance_to_triangle(*this);
}

point_2d_t triangle_2d_t::point_from_barycentric_coords(
    const barycentric_coordinates_t &b) const {
    return p1 * b.u + p2 * b.v + p3 * b.w;
}

std::string triangle_2d_t::to_string() const {
    std::ostringstream ss;
    ss << "Triangle2D(" << p1.to_string() << ", " << p2.to_string() << ", "
       << p3.to_string() << ")";
    return ss.str();
}

/* ----------- *
 * circle_2d_t *
 * ----------- */

circle_2d_t::circle_2d_t() : center({0.0, 0.0}), radius(0.0) {}

circle_2d_t::circle_2d_t(const point_2d_t &c, double r) {
    center = c;
    radius = r;
}

circle_2d_t::circle_2d_t(const triangle_2d_t &t) {
    point_2d_t p1 = t.p1, p2 = t.p2, p3 = t.p3;
    double a = p2.x - p1.x;
    double b = p2.y - p1.y;
    double c = p3.x - p1.x;
    double d = p3.y - p1.y;
    double e = a * (p1.x + p2.x) + b * (p1.y + p2.y);
    double f = c * (p1.x + p3.x) + d * (p1.y + p3.y);
    double g = 2.0 * (a * (p3.y - p2.y) - b * (p3.x - p2.x));
    center = {(d * e - b * f) / g, (a * f - c * e) / g};
    radius = center.distance_to_point(p1);
}

bool circle_2d_t::operator==(const circle_2d_t &c) const {
    return center == c.center && std::abs(radius - c.radius) < get_tolerance();
}

bool circle_2d_t::operator!=(const circle_2d_t &c) const {
    return !(*this == c);
}

double circle_2d_t::area() const { return M_PI * radius * radius; }

double circle_2d_t::circumference() const { return 2.0 * M_PI * radius; }

bool circle_2d_t::contains_point(const point_2d_t &p, double tolerance) const {
    return center.distance_to_point(p) <= radius + tolerance;
}

std::vector<point_2d_t> circle_2d_t::intersection(const circle_2d_t &c) const {
    std::vector<point_2d_t> points;
    double d = center.distance_to_point(c.center);
    if (d + get_tolerance() > radius + c.radius) return points;
    if (d - get_tolerance() < std::abs(radius - c.radius)) return points;
    double a = (radius * radius - c.radius * c.radius + d * d) / (2.0 * d);
    double h = std::sqrt(radius * radius - a * a);
    point_2d_t p2 = center + (c.center - center) * (a / d);
    point_2d_t p3 = p2 + (c.center - center).perpendicular() * (h / d);
    points.push_back(p3);
    if (h > get_tolerance()) {
        p3 = p2 - (c.center - center).perpendicular() * (h / d);
        points.push_back(p3);
    }
    return points;
}

std::string circle_2d_t::to_string() const {
    std::ostringstream ss;
    ss << "Circle2D(" << center.to_string() << ", " << radius << ")";
    return ss.str();
}

/* ----------------- *
 * bounding_box_2d_t *
 * ----------------- */

bounding_box_2d_t::bounding_box_2d_t() {
    min = {std::numeric_limits<double>::max(),
           std::numeric_limits<double>::max()};
    max = {std::numeric_limits<double>::lowest(),
           std::numeric_limits<double>::lowest()};
}

bounding_box_2d_t::bounding_box_2d_t(const point_2d_t &p1,
                                     const point_2d_t &p2) {
    min = {std::min(p1.x, p2.x), std::min(p1.y, p2.y)};
    max = {std::max(p1.x, p2.x), std::max(p1.y, p2.y)};
}

bounding_box_2d_t::bounding_box_2d_t(const std::vector<point_2d_t> &points) {
    if (points.empty()) throw std::runtime_error("Empty point list");

    double min_x = points[0].x, min_y = points[0].y;
    double max_x = points[0].x, max_y = points[0].y;

    for (size_t i = 1; i < points.size(); ++i) {
        min_x = std::min(min_x, points[i].x);
        min_y = std::min(min_y, points[i].y);
        max_x = std::max(max_x, points[i].x);
        max_y = std::max(max_y, points[i].y);
    }

    min = {min_x, min_y};
    max = {max_x, max_y};
}

bounding_box_2d_t::bounding_box_2d_t(const std::vector<line_2d_t> &lines) {
    if (lines.empty()) throw std::runtime_error("Empty line list");

    double min_x = lines[0].p1.x, min_y = lines[0].p1.y;
    double max_x = lines[0].p1.x, max_y = lines[0].p1.y;

    for (size_t i = 0; i < lines.size(); ++i) {
        min_x = std::min(min_x, lines[i].p1.x);
        min_y = std::min(min_y, lines[i].p1.y);
        max_x = std::max(max_x, lines[i].p1.x);
        max_y = std::max(max_y, lines[i].p1.y);

        min_x = std::min(min_x, lines[i].p2.x);
        min_y = std::min(min_y, lines[i].p2.y);
        max_x = std::max(max_x, lines[i].p2.x);
        max_y = std::max(max_y, lines[i].p2.y);
    }

    min = {min_x, min_y};
    max = {max_x, max_y};
}

bounding_box_2d_t::bounding_box_2d_t(
    const std::vector<triangle_2d_t> &triangles) {
    if (triangles.empty()) throw std::runtime_error("Empty triangle list");

    double min_x = triangles[0].p1.x, min_y = triangles[0].p1.y;
    double max_x = triangles[0].p1.x, max_y = triangles[0].p1.y;

    for (size_t i = 0; i < triangles.size(); ++i) {
        min_x = std::min(min_x, triangles[i].p1.x);
        min_y = std::min(min_y, triangles[i].p1.y);
        max_x = std::max(max_x, triangles[i].p1.x);
        max_y = std::max(max_y, triangles[i].p1.y);

        min_x = std::min(min_x, triangles[i].p2.x);
        min_y = std::min(min_y, triangles[i].p2.y);
        max_x = std::max(max_x, triangles[i].p2.x);
        max_y = std::max(max_y, triangles[i].p2.y);

        min_x = std::min(min_x, triangles[i].p3.x);
        min_y = std::min(min_y, triangles[i].p3.y);
        max_x = std::max(max_x, triangles[i].p3.x);
        max_y = std::max(max_y, triangles[i].p3.y);
    }

    min = {min_x, min_y};
    max = {max_x, max_y};
}

bounding_box_2d_t::bounding_box_2d_t(
    const std::vector<bounding_box_2d_t> &bboxes) {
    if (bboxes.empty()) throw std::runtime_error("Empty bounding box list");

    double min_x = bboxes[0].min.x, min_y = bboxes[0].min.y;
    double max_x = bboxes[0].max.x, max_y = bboxes[0].max.y;

    for (size_t i = 1; i < bboxes.size(); ++i) {
        min_x = std::min(min_x, bboxes[i].min.x);
        min_y = std::min(min_y, bboxes[i].min.y);
        max_x = std::max(max_x, bboxes[i].max.x);
        max_y = std::max(max_y, bboxes[i].max.y);
    }

    min = {min_x, min_y};
    max = {max_x, max_y};
}

bool bounding_box_2d_t::operator==(const bounding_box_2d_t &b) const {
    return min == b.min && max == b.max;
}

bool bounding_box_2d_t::operator!=(const bounding_box_2d_t &b) const {
    return min != b.min || max != b.max;
}

bounding_box_2d_t bounding_box_2d_t::operator<<=(const affine_2d_t &a) {
    min <<= a;
    max <<= a;
    return *this;
}

double bounding_box_2d_t::area() const {
    return (max.x - min.x) * (max.y - min.y);
}

point_2d_t bounding_box_2d_t::center() const {
    return {(min.x + max.x) / 2.0, (min.y + max.y) / 2.0};
}

std::vector<point_2d_t> bounding_box_2d_t::vertices() const {
    return {min, {max.x, min.y}, max, {min.x, max.y}};
}

std::vector<line_2d_t> bounding_box_2d_t::edges() const {
    return {{min, {max.x, min.y}},
            {{max.x, min.y}, max},
            {max, {min.x, max.y}},
            {{min.x, max.y}, min}};
}

bool bounding_box_2d_t::intersects_triangle(const triangle_2d_t &t) const {
    for (const auto &l : edges())
        if (l.intersects_triangle(t)) return true;
    return false;
}

bool bounding_box_2d_t::contains_point(const point_2d_t &p) const {
    return p.x >= min.x - get_tolerance() && p.x <= max.x + get_tolerance() &&
           p.y >= min.y - get_tolerance() && p.y <= max.y + get_tolerance();
}

bool bounding_box_2d_t::contains_triangle(const triangle_2d_t &t) const {
    return contains_point(t.p1) && contains_point(t.p2) && contains_point(t.p3);
}

double bounding_box_2d_t::distance_to_point(const point_2d_t &p) const {
    if (p.is_inside_bounding_box(*this)) return 0.0;
    return std::min({p.distance_to_line({min, {max.x, min.y}}),
                     p.distance_to_line({{max.x, min.y}, max}),
                     p.distance_to_line({max, {min.x, max.y}}),
                     p.distance_to_line({{min.x, max.y}, min})});
}

double bounding_box_2d_t::distance_to_line(const line_2d_t &l) const {
    if (l.p1.is_inside_bounding_box(*this) ||
        l.p2.is_inside_bounding_box(*this))
        return 0.0;
    return std::min({l.distance_to_line({min, {max.x, min.y}}),
                     l.distance_to_line({{max.x, min.y}, max}),
                     l.distance_to_line({max, {min.x, max.y}}),
                     l.distance_to_line({{min.x, max.y}, min})});
}

double bounding_box_2d_t::distance_to_triangle(const triangle_2d_t &t) const {
    if (t.p1.is_inside_bounding_box(*this) ||
        t.p2.is_inside_bounding_box(*this) ||
        t.p3.is_inside_bounding_box(*this))
        return 0.0;
    return std::min({t.distance_to_line({min, {max.x, min.y}}),
                     t.distance_to_line({{max.x, min.y}, max}),
                     t.distance_to_line({max, {min.x, max.y}}),
                     t.distance_to_line({{min.x, max.y}, min})});
}

double bounding_box_2d_t::distance_to_bounding_box(
    const bounding_box_2d_t &b) const {
    point_2d_t p1 = min, p2 = {max.x, min.y}, p3 = max, p4 = {min.x, max.y};
    if (p1.is_inside_bounding_box(b) || p2.is_inside_bounding_box(b) ||
        p3.is_inside_bounding_box(b) || p4.is_inside_bounding_box(b))
        return 0.0;
    return std::min({b.distance_to_line({p1, p2}), b.distance_to_line({p2, p3}),
                     b.distance_to_line({p3, p4}),
                     b.distance_to_line({p4, p1})});
}

std::string bounding_box_2d_t::to_string() const {
    std::ostringstream ss;
    ss << "BoundingBox2D(" << min.to_string() << ", " << max.to_string() << ")";
    return ss.str();
}

/* ------------ *
 * polygon_2d_t *
 * ------------ */

polygon_2d_t::polygon_2d_t(const std::vector<point_2d_t> &ps) : points(ps) {
    if (points.size() < 3)
        throw std::runtime_error("polygon_2d_t must have at least 3 points");
}

bool polygon_2d_t::operator==(const polygon_2d_t &p) const {
    return points == p.points;
}

bool polygon_2d_t::operator!=(const polygon_2d_t &p) const {
    return points != p.points;
}

polygon_2d_t polygon_2d_t::operator<<=(const affine_2d_t &a) {
    for (auto &p : points) p <<= a;
    return *this;
}

polygon_2d_t polygon_2d_t::operator+(const polygon_2d_t &p) const {
    polygon_2d_t result = *this;
    result += p;
    return result;
}

polygon_2d_t polygon_2d_t::operator+=(const polygon_2d_t &p) {
    points.insert(points.end(), p.points.begin(), p.points.end());
    return *this;
}

double polygon_2d_t::signed_area() const {
    double area = 0.0;
    for (size_t i = 0; i < points.size(); ++i) {
        const point_2d_t &p1 = points[i];
        const point_2d_t &p2 = points[(i + 1) % points.size()];
        area += (p1.x * p2.y - p2.x * p1.y);
    }
    return area * 0.5f;
}

bool polygon_2d_t::is_clockwise() const { return signed_area() < 0.0; }

void polygon_2d_t::reverse() { std::reverse(points.begin(), points.end()); }

polygon_2d_t polygon_2d_t::convex_hull() const {
    int n = points.size();
    if (n <= 3) return *this;

    // Finds convex hull using Graham Scan algorithm.
    // https://en.wikipedia.org/wiki/Graham_scan

    // Find the lowest y-coordinate and leftmost point, called P0.
    int P0 = 0;
    for (int i = 1; i < n; i++) {
        auto &[x, y] = points[i];
        auto &[x0, y0] = points[P0];
        if (y < y0 || (y == y0 && x < x0)) P0 = i;
    }

    // Sort points by polar angle with P0, in clockwise order.
    std::vector<int> hull_points(n);
    std::iota(hull_points.begin(), hull_points.end(), 0);
    std::sort(hull_points.begin(), hull_points.end(), [&](int i, int j) {
        if (i == P0) return true;  // First element.
        double det =
            (points[i] - points[P0]).determinant(points[j] - points[P0]);
        if (det == 0)
            return points[i].distance_to_point(points[P0]) <
                   points[j].distance_to_point(points[P0]);
        return det > 0;
    });

    // Traverses the points, keeping points which are convex.
    std::vector<point_2d_t> stack;
    for (int i = 0; i < n; i++) {
        int point = hull_points[i];
        while (stack.size() > 1 &&
               (stack[stack.size() - 2] - stack.back())
                       .determinant(points[point] - stack.back()) >= 0) {
            stack.pop_back();
        }
        stack.push_back(points[point]);
    }

    // Ensures that the last point is also convex.
    while (stack.size() > 2 &&
           (stack[stack.size() - 2] - stack.back())
                   .determinant(stack[0] - stack.back()) >= 0) {
        stack.pop_back();
    }

    return {stack};
}

bounding_box_2d_t polygon_2d_t::bounding_box() const {
    double min_x = points[0].x, min_y = points[0].y;
    double max_x = points[0].x, max_y = points[0].y;
    for (const auto &p : points) {
        min_x = std::min(min_x, p.x);
        min_y = std::min(min_y, p.y);
        max_x = std::max(max_x, p.x);
        max_y = std::max(max_y, p.y);
    }
    return {{min_x, min_y}, {max_x, max_y}};
}

point_2d_t polygon_2d_t::center() const {
    point_2d_t center;
    for (const auto &p : points) center += p;
    center /= points.size();
    return center;
}

bool is_ear(const bvh_2d_t &bvh, const std::vector<point_2d_t> &points, int vi,
            int vj, int vk) {
    point_2d_t pi = points[vi], pj = points[vj], pk = points[vk];

    // Checks if the triangle is convex.
    if (!is_convex(pi, pj, pk)) return false;

    // Checks if the triangle contains any other points.

    // Linear complexity version, slow.
    // for (int l = 0; l < points.size(); l++) {
    //     if (l == vi || l == vj || l == vk) continue;
    //     triangle_2d_t triangle{pi, pj, pk};
    //     if (points[l].is_inside_triangle(triangle)) return false;
    // }

    // Faster version using BVH.
    const auto &intrs =
        bvh.triangle_intersections({pi, pj, pk}, /* max_intersections */ 4);
    for (const auto &intr : intrs) {
        auto l = intr.a;  // a, b, c are all the same for this BVH.
        if (l == vi || l == vj || l == vk) continue;
        return false;
    }

    return true;
}

trimesh_2d_t polygon_2d_t::get_trimesh(bool delaunay, bool is_convex) const {
    if (points.size() < 3) throw std::runtime_error("Invalid polygon.");

    // Gets the vertex indices from 0 to n - 1.
    std::vector<size_t> indices(points.size());
    std::iota(indices.begin(), indices.end(), 0);

    // Ensures that the polygon is counter-clockwise.
    if (is_clockwise()) {
        std::reverse(indices.begin(), indices.end());
    }

    std::vector<point_2d_t> vertices(points);
    face_list_t faces;

    // Builds a BVH where each face is a single point.
    face_list_t bvh_faces;
    for (size_t i = 0; i < points.size(); i++) {
        bvh_faces.push_back({i, i, i});
    }
    bvh_2d_t bvh{bvh_faces, vertices};

    // Runs ear clipping algorithm.
    while (indices.size() > 3) {
        bool found = false;
        size_t n = indices.size();
        for (size_t i = 0; i < n; i++) {
            size_t j = (i + 1) % n;
            size_t k = (i + 2) % n;
            size_t vi = indices[i], vj = indices[j], vk = indices[k];
            if (is_convex || is_ear(bvh, points, vi, vj, vk)) {
                faces.push_back({vi, vj, vk});
                indices.erase(indices.begin() + j);
                found = true;
                break;
            }
        }
        if (!found) {
            throw std::runtime_error("Unable to triangulate polygon.");
        }
    }
    faces.push_back({indices[0], indices[1], indices[2]});

    const trimesh_2d_t trimesh{vertices, faces};
    return delaunay ? trimesh.make_delaunay() : trimesh;
}

std::string polygon_2d_t::to_string() const {
    std::ostringstream ss;
    ss << "Polygon2D(" << points.size() << " vertices)";
    return ss.str();
}

/* ----------- *
 * affine_2d_t *
 * ----------- */

affine_2d_t::affine_2d_t(std::optional<double> rot,
                         std::optional<std::tuple<double, double>> trans,
                         std::optional<double> scale) {
    if (rot) {
        double c = std::cos(*rot);
        double s = std::sin(*rot);
        r00 = c;
        r01 = -s;
        r10 = s;
        r11 = c;
    } else {
        r00 = 1.0;
        r01 = 0.0;
        r10 = 0.0;
        r11 = 1.0;
    }

    if (trans) {
        auto [x, y] = *trans;
        tx = x;
        ty = y;
    } else {
        tx = 0.0;
        ty = 0.0;
    }

    if (scale) {
        r00 *= *scale;
        r01 *= *scale;
        r10 *= *scale;
        r11 *= *scale;
    }
}

affine_2d_t::affine_2d_t(
    std::tuple<std::tuple<double, double>, std::tuple<double, double>> rot,
    std::tuple<double, double> trans)
    : r00(std::get<0>(std::get<0>(rot))),
      r01(std::get<0>(std::get<1>(rot))),
      r10(std::get<1>(std::get<0>(rot))),
      r11(std::get<1>(std::get<1>(rot))),
      tx(std::get<0>(trans)),
      ty(std::get<1>(trans)) {}

affine_2d_t affine_2d_t::operator*=(const affine_2d_t &a) {
    double r00_ = r00 * a.r00 + r01 * a.r10;
    double r01_ = r00 * a.r01 + r01 * a.r11;
    double r10_ = r10 * a.r00 + r11 * a.r10;
    double r11_ = r10 * a.r01 + r11 * a.r11;
    double tx_ = tx * a.r00 + ty * a.r10 + a.tx;
    double ty_ = tx * a.r01 + ty * a.r11 + a.ty;
    r00 = r00_;
    r01 = r01_;
    r10 = r10_;
    r11 = r11_;
    tx = tx_;
    ty = ty_;
    return *this;
}

affine_2d_t affine_2d_t::inverse() const {
    double det = r00 * r11 - r01 * r10;
    double r00_ = r11 / det;
    double r01_ = -r01 / det;
    double r10_ = -r10 / det;
    double r11_ = r00 / det;
    double tx_ = (r10 * ty - r11 * tx) / det;
    double ty_ = (r01 * tx - r00 * ty) / det;
    return {{{r00_, r01_}, {r10_, r11_}}, {tx_, ty_}};
}

std::tuple<std::tuple<double, double>, std::tuple<double, double>>
affine_2d_t::rotation() const {
    return {{r00, r01}, {r10, r11}};
}

std::tuple<double, double> affine_2d_t::translation() const { return {tx, ty}; }

std::string affine_2d_t::to_string() const {
    std::ostringstream ss;
    ss << "Affine2D(((" << r00 << ", " << r01 << "), (" << r10 << ", " << r11
       << ")), (" << tx << ", " << ty << "))";
    return ss.str();
}

affine_2d_t operator*(const affine_2d_t &a1, const affine_2d_t &a2) {
    affine_2d_t a = a1;
    a *= a2;
    return a;
}

point_2d_t operator>>(const affine_2d_t &a, const point_2d_t &p) {
    return {a.r00 * p.x + a.r01 * p.y + a.tx, a.r10 * p.x + a.r11 * p.y + a.ty};
}

point_2d_t operator<<(const point_2d_t &p, const affine_2d_t &a) {
    return {a.r00 * p.x + a.r01 * p.y + a.tx, a.r10 * p.x + a.r11 * p.y + a.ty};
}

line_2d_t operator>>(const affine_2d_t &a, const line_2d_t &l) {
    return {a >> l.p1, a >> l.p2};
}

line_2d_t operator<<(const line_2d_t &l, const affine_2d_t &a) {
    return a >> l;
}

triangle_2d_t operator>>(const affine_2d_t &a, const triangle_2d_t &t) {
    return {a >> t.p1, a >> t.p2, a >> t.p3};
}

triangle_2d_t operator<<(const triangle_2d_t &t, const affine_2d_t &a) {
    return a >> t;
}

bounding_box_2d_t operator>>(const affine_2d_t &a,
                             const bounding_box_2d_t &bb) {
    return {a >> bb.min, a >> bb.max};
}

bounding_box_2d_t operator<<(const bounding_box_2d_t &bb,
                             const affine_2d_t &a) {
    return a >> bb;
}

polygon_2d_t operator>>(const affine_2d_t &a, const polygon_2d_t &p) {
    std::vector<point_2d_t> points;
    for (const auto &p1 : p.points) points.push_back(a >> p1);
    return {points};
}

polygon_2d_t operator<<(const polygon_2d_t &p, const affine_2d_t &a) {
    return a >> p;
}

/* ------------ *
 * trimesh_2d_t *
 * ------------ */

trimesh_2d_t::trimesh_2d_t(const std::vector<point_2d_t> &vertices,
                           const face_set_t &faces, bool validate)
    : _vertices(vertices), _faces(faces.begin(), faces.end()) {
    if (validate) this->validate();
}

trimesh_2d_t::trimesh_2d_t(const std::vector<point_2d_t> &vertices,
                           const face_list_t &faces, bool validate)
    : _vertices(vertices), _faces(faces) {
    if (validate) this->validate();
}

void trimesh_2d_t::validate() const {
    // Checks that there is at least one face.
    if (_faces.empty()) {
        throw std::invalid_argument("No faces");
    }

    // Checks that all face vertices are valid.
    for (auto &face : _faces) {
        auto &[vi, vj, vk] = face;
        if (vi >= _vertices.size() || vj >= _vertices.size() ||
            vk >= _vertices.size()) {
            throw std::invalid_argument(
                "Invalid face: " + face.to_string() + " for " +
                std::to_string(_vertices.size()) + " vertices");
        }
    }

    // Checks that all vertices are used.
    std::vector<bool> used(_vertices.size(), false);
    for (auto &face : _faces) {
        auto &[vi, vj, vk] = face;
        used[vi] = true;
        used[vj] = true;
        used[vk] = true;
    }
    for (size_t i = 0; i < used.size(); i++) {
        if (!used[i]) {
            throw std::invalid_argument("Unused vertex: " + std::to_string(i));
        }
    }

    // Checks that all faces are triangles.
    for (auto &face : _faces) {
        auto &[vi, vj, vk] = face;
        if (vi == vj || vi == vk || vj == vk) {
            throw std::invalid_argument("Face is not a triangle");
        }
    }

    // Checks that all 2D faces are oriented the same direction.
    auto &face = _faces[0];
    auto &[vi, vj, vk] = face;
    const point_2d_t &p1 = _vertices[vi], &p2 = _vertices[vj],
                     &p3 = _vertices[vk];
    const point_2d_t v1 = p2 - p1, v2 = p3 - p1;
    double normal = v1.cross(v2);
    for (auto &face : _faces) {
        auto &[vi, vj, vk] = face;
        const point_2d_t &p1 = _vertices[vi], &p2 = _vertices[vj],
                         &p3 = _vertices[vk];
        const point_2d_t v1 = p2 - p1, v2 = p3 - p1;
        double normal1 = v1.cross(v2);
        if (normal * normal1 < 0) {
            throw std::invalid_argument("Face is not oriented the same way");
        }
    }
}

const std::vector<point_2d_t> &trimesh_2d_t::vertices() const {
    return _vertices;
}

const face_list_t &trimesh_2d_t::faces() const { return _faces; }

const triangle_2d_t trimesh_2d_t::get_triangle(const face_t &face) const {
    auto &[vi, vj, vk] = face;
    return {_vertices[vi], _vertices[vj], _vertices[vk]};
}

const std::vector<triangle_2d_t> trimesh_2d_t::get_triangles() const {
    std::vector<triangle_2d_t> result;
    for (auto &face : _faces) {
        result.push_back(get_triangle(face));
    }
    return result;
}

const std::tuple<std::vector<point_2d_t>, face_set_t>
trimesh_2d_t::merge_vertices(const std::vector<point_2d_t> &vertices,
                             const face_set_t &faces) {
    std::vector<point_2d_t> new_vertices;
    std::map<point_2d_t, size_t> vertex_map;
    for (auto &v : vertices) {
        if (vertex_map.find(v) == vertex_map.end()) {
            vertex_map[v] = new_vertices.size();
            new_vertices.push_back(v);
        }
    }

    face_set_t new_faces;
    for (auto &face : faces) {
        auto &[vi, vj, vk] = face;
        new_faces.insert({vertex_map[vertices[vi]], vertex_map[vertices[vj]],
                          vertex_map[vertices[vk]]});
    }

    return {new_vertices, new_faces};
}

const std::tuple<std::vector<point_2d_t>, face_set_t>
trimesh_2d_t::remove_unused_vertices(const std::vector<point_2d_t> &vertices,
                                     const face_set_t &faces) {
    std::unordered_map<size_t, size_t> vertex_id_map;
    for (auto f : faces) {
        vertex_id_map[f.a] = 0;
        vertex_id_map[f.b] = 0;
        vertex_id_map[f.c] = 0;
    }
    std::vector<point_2d_t> new_vertices;
    for (auto &[old_id, new_id] : vertex_id_map) {
        new_id = new_vertices.size();
        new_vertices.push_back(vertices[old_id]);
    }
    face_set_t new_faces;
    for (auto f : faces) {
        const auto &a = new_vertices[vertex_id_map[f.a]],
                   &b = new_vertices[vertex_id_map[f.b]],
                   &c = new_vertices[vertex_id_map[f.c]];

        if ((b - a).cross(c - a) < 0) {
            new_faces.insert(
                {vertex_id_map[f.a], vertex_id_map[f.c], vertex_id_map[f.b]});
        } else {
            new_faces.insert(
                {vertex_id_map[f.a], vertex_id_map[f.b], vertex_id_map[f.c]});
        }
    }
    return {new_vertices, new_faces};
}

const std::tuple<std::vector<point_2d_t>, face_set_t>
trimesh_2d_t::merge_triangles(const std::vector<point_2d_t> &init_vertices,
                              const face_set_t &init_faces) {
    bool changed = true;

    std::vector<point_2d_t> new_vertices = init_vertices;
    face_set_t new_faces = init_faces;

    while (changed) {
        changed = false;

        const std::vector<point_2d_t> vertices(new_vertices.begin(),
                                               new_vertices.end());
        face_list_t face_list(new_faces.begin(), new_faces.end());

        // Clears the new vertices and faces.
        new_vertices.clear();
        new_faces.clear();

        // Gets the number of faces for each vertex.
        std::vector<size_t> num_vertex_faces(vertices.size(), 0);
        for (const auto &face : face_list) {
            num_vertex_faces[face.a]++;
            num_vertex_faces[face.b]++;
            num_vertex_faces[face.c]++;
        }

        // Gets edges for adjacent faces.
        std::unordered_map<edge_t, std::vector<size_t>, __edge_hash_fn> adj_map;
        for (size_t i = 0; i < face_list.size(); i++) {
            for (const auto &edge : face_list[i].get_edges(false)) {
                adj_map[edge].push_back(i);
            }
        }

        // Gets the true face ID, after having been merged.
        std::vector<int> new_face_id(face_list.size(), -1);
        auto get_face_id = [&new_face_id](const size_t &face_id) {
            size_t i = face_id;
            while (true) {
                if (new_face_id[i] == -1) return i;
                i = new_face_id[i];
            }
        };

        std::queue<edge_t> edge_queue;
        for (auto &[edge, adj] : adj_map) {
            if (adj.size() > 2) {
                std::stringstream ss;
                ss << "Non-manifold mesh; got " << adj.size()
                   << " adjacent faces for edge " << edge.to_string() << ":";
                for (auto &face_id : adj) {
                    auto &face = face_list[face_id];
                    ss << " " << face.to_string();
                }
                throw std::runtime_error(ss.str());
            }
            if (adj.size() == 2) edge_queue.push(edge);
        }

        // Checks each shared edge to see if it can be merged. The edge can be
        // merged if any of the two other edges of the adjacent faces
        // colinear. If so, then mark the face as unused, and add a pointer to
        // the new face to the adjacent faces.
        while (!edge_queue.empty()) {
            auto edge = edge_queue.front();
            edge_queue.pop();
            if (adj_map.find(edge) == adj_map.end()) continue;
            const auto &adj_faces = adj_map[edge];
            auto f1 = get_face_id(adj_faces[0]), f2 = get_face_id(adj_faces[1]);
            if (f1 == f2) continue;

            // Gets the point for each face that is not on the edge.
            if (!face_list[f1].has_edge(edge) || !face_list[f2].has_edge(edge))
                continue;
            auto o1 = face_list[f1].get_other_vertex(edge),
                 o2 = face_list[f2].get_other_vertex(edge);
            auto &va = vertices[edge.a], &vb = vertices[edge.b];
            auto &v1 = vertices[o1], &v2 = vertices[o2];

            // Checks if either edge point is colinear with the two
            // other points. If so, create a new face with the
            // remaining point, and mark the two old faces as merged.
            bool a_colinear =
                     std::abs((v1 - va).normalize().cross(
                         (v2 - va).normalize())) < std::sqrt(get_tolerance()) &&
                     num_vertex_faces[edge.a] == 2,
                 b_colinear =
                     std::abs((v1 - vb).normalize().cross(
                         (v2 - vb).normalize())) < std::sqrt(get_tolerance()) &&
                     num_vertex_faces[edge.b] == 2;
            if (!a_colinear && !b_colinear) continue;

            // Creates a new face.
            face_t new_face{o1, o2, a_colinear ? edge.b : edge.a};
            face_list.push_back(new_face);
            new_face_id.push_back(-1);
            new_face_id[f1] = face_list.size() - 1;
            new_face_id[f2] = face_list.size() - 1;
            changed = true;

            // Reconsiders the edges of the new face.
            for (const auto &new_edge : new_face.get_edges(false))
                edge_queue.push(new_edge);
        }

        // Gets all vertices that are used by the new faces.
        std::unordered_map<size_t, size_t> vertex_id_map;
        for (size_t i = 0; i < face_list.size(); i++) {
            if (new_face_id[i] != -1) continue;
            auto &f = face_list[i];
            vertex_id_map[f.a] = 0;
            vertex_id_map[f.b] = 0;
            vertex_id_map[f.c] = 0;
        }
        for (auto &[old_id, new_id] : vertex_id_map) {
            new_id = new_vertices.size();
            new_vertices.push_back(vertices[old_id]);
        }

        // Remaps the vertex ids in the new faces.
        for (size_t i = 0; i < face_list.size(); i++) {
            if (new_face_id[i] != -1) continue;
            auto &f = face_list[i];
            const auto &a = new_vertices[vertex_id_map[f.a]],
                       &b = new_vertices[vertex_id_map[f.b]],
                       &c = new_vertices[vertex_id_map[f.c]];

            if ((b - a).cross(c - a) < 0) {
                new_faces.insert({vertex_id_map[f.a], vertex_id_map[f.c],
                                  vertex_id_map[f.b]});
            } else {
                new_faces.insert({vertex_id_map[f.a], vertex_id_map[f.b],
                                  vertex_id_map[f.c]});
            }
        }
    }

    return {new_vertices, new_faces};
}

const std::vector<face_set_t> trimesh_2d_t::get_connected_components() const {
    std::vector<face_set_t> result;

    // Build adjacency matrix.
    std::vector<std::unordered_set<size_t>> adj;
    adj.resize(_vertices.size());
    for (size_t i = 0; i < _faces.size(); i++) {
        auto &[a, b, c] = _faces[i];
        adj[a].insert(i);
        adj[b].insert(i);
        adj[c].insert(i);
    }

    // Flood fills to get connected components for each face.
    std::vector<bool> used(_faces.size(), false);

    auto add_all_adj_faces = [&](const size_t &vertex_id,
                                 std::queue<size_t> &queue) {
        for (auto &adj_face_id : adj[vertex_id]) {
            if (!used[adj_face_id]) {
                used[adj_face_id] = true;
                queue.push(adj_face_id);
            }
        }
    };

    for (size_t face_id = 0; face_id < _faces.size(); face_id++) {
        if (used[face_id]) continue;
        face_set_t cur_faces;
        std::queue<size_t> queue;
        queue.push(face_id);
        while (!queue.empty()) {
            size_t cur_face_id = queue.front();
            queue.pop();
            cur_faces.insert(_faces[cur_face_id]);
            auto &[a, b, c] = _faces[cur_face_id];
            add_all_adj_faces(a, queue);
            add_all_adj_faces(b, queue);
            add_all_adj_faces(c, queue);
        }
        result.push_back(cur_faces);
    }

    return result;
}

const std::vector<std::tuple<polygon_2d_t, std::vector<size_t>>>
trimesh_2d_t::get_polygon(const face_set_t &component) const {
    auto get_abs_angle = [](const point_2d_t &a, const point_2d_t &b,
                            const point_2d_t &c) {
        double angle = (b - a).angle(c - a);
        if (angle < 0) angle += 2 * M_PI;
        auto rad_angle = std::min(angle, 2 * M_PI - angle);
        auto deg_angle = (rad_angle * 180 / M_PI);
        return (double)deg_angle;
    };

    // First, gets the sum of the angles at each vertex.
    std::unordered_map<size_t, double> angles;
    for (const auto &face : component) {
        auto &[a, b, c] = face;
        auto &va = _vertices[a], &vb = _vertices[b], &vc = _vertices[c];
        angles[a] += get_abs_angle(va, vb, vc);
        angles[b] += get_abs_angle(vb, vc, va);
        angles[c] += get_abs_angle(vc, va, vb);
    }

    // Determine if each vertex is a boundary vertex.
    std::unordered_set<size_t> boundary_pts;
    for (auto &[i, angle] : angles) {
        if (std::abs(angles[i] - 360.0) > 0.1f) {
            boundary_pts.insert(i);
        }
    }

    auto is_boundary = [&](const size_t &vertex) {
        return boundary_pts.find(vertex) != boundary_pts.end();
    };

    // Builds a BVH for the faces.
    face_list_t faces(component.begin(), component.end());
    bvh_2d_t bvh(faces, _vertices);

    auto intersects_another_edge = [&](const edge_t &edge,
                                       const face_set_t &component) {
        // The O(n^2) version checks all edges against all other edges.
        // Using a BVH speeds this up to O(n log(n)).
        // for (const auto &face : component) {
        line_2d_t line{_vertices[edge.a], _vertices[edge.b]};
        for (const auto &face :
             bvh.line_intersections(line, /* max_intersections */ 3)) {
            for (auto &other_edge : face.get_edges(false)) {
                if (edge.a == other_edge.a || edge.a == other_edge.b ||
                    edge.b == other_edge.a || edge.b == other_edge.b) {
                    continue;
                }

                line_2d_t line_a{_vertices[edge.a], _vertices[edge.b]},
                    line_b{_vertices[other_edge.a], _vertices[other_edge.b]};
                if (line_a.line_intersection(line_b).has_value()) return true;
            }
        }
        return false;
    };

    // Counts number of edges between boundary vertices.
    edge_map_t<size_t> edge_counts;
    for (const auto &face : component) {
        for (auto &edge : face.get_edges(false)) {
            if (is_boundary(edge.a) && is_boundary(edge.b)) {
                edge_counts[edge]++;
            }
        }
    }

    // Next, get the adjacencies between boundary vertices. Don't include
    // edges that are shared by more than one face.
    std::unordered_map<size_t, std::unordered_set<size_t>> adjacencies;
    for (const auto &face : component) {
        for (auto &edge : face.get_edges(false)) {
            if (is_boundary(edge.a) && is_boundary(edge.b) &&
                edge_counts[edge] == 1 &&
                !intersects_another_edge(edge, component)) {
                adjacencies[edge.a].insert(edge.b);
                adjacencies[edge.b].insert(edge.a);
            }
        }
    }

    // Flood fills to get vertices that are part of the same polygon.
    std::unordered_set<size_t> used;
    std::vector<std::vector<size_t>> polygon_inds;
    for (auto &[vertex, adj_vertices] : adjacencies) {
        if (used.find(vertex) != used.end()) continue;
        std::stack<size_t> stack;
        stack.push(vertex);
        used.insert(vertex);
        std::vector<size_t> cur_polygon_inds;
        while (!stack.empty()) {
            size_t cur_vertex = stack.top();
            stack.pop();
            cur_polygon_inds.push_back(cur_vertex);
            for (auto &adj_vertex : adjacencies[cur_vertex]) {
                if (used.find(adj_vertex) != used.end()) continue;
                used.insert(adj_vertex);
                stack.push(adj_vertex);
            }
        }
        polygon_inds.push_back(cur_polygon_inds);
    }

    // Gets the polygons for each set of vertices.
    std::vector<std::tuple<polygon_2d_t, std::vector<size_t>>> return_val;
    for (auto &cur_polygon_inds : polygon_inds) {
        std::vector<point_2d_t> polygon_vertices;

        auto is_colinear = [&](const point_2d_t &p) {
            if (polygon_vertices.size() <= 1) return false;
            auto &p1 = polygon_vertices[polygon_vertices.size() - 2],
                 &p2 = polygon_vertices[polygon_vertices.size() - 1];
            return std::abs((p1 - p2).cross(p - p2)) < get_tolerance();
        };

        for (auto &ind : cur_polygon_inds) {
            auto &p = _vertices[ind];
            if (is_colinear(p)) polygon_vertices.pop_back();
            polygon_vertices.push_back(p);
        }

        if (is_colinear(polygon_vertices[0])) polygon_vertices.pop_back();
        if (polygon_vertices.size() < 3) continue;
        polygon_2d_t polygon{polygon_vertices};
        return_val.push_back({polygon, cur_polygon_inds});
    }

    return return_val;
}

const std::vector<std::tuple<polygon_2d_t, std::vector<size_t>>>
trimesh_2d_t::get_polygons() const {
    auto connected_components = get_connected_components();
    std::vector<std::tuple<polygon_2d_t, std::vector<size_t>>> result;
    for (auto &face : connected_components) {
        const auto &polygon = get_polygon(face);
        result.insert(result.end(), polygon.begin(), polygon.end());
    }
    return result;
}

trimesh_2d_t trimesh_2d_t::subdivide(bool at_edges) const {
    std::vector<point_2d_t> vertices = _vertices;
    face_list_t faces;

    if (at_edges) {
        // Add center points of each edge as new vertices.
        std::map<const std::tuple<size_t, size_t>, size_t> edge_map;
        auto add_edge = [&](const size_t &p1, const size_t &p2) {
            std::tuple<size_t, size_t> edge1 = {p1, p2}, edge2 = {p2, p1};
            if (edge_map.find(edge1) == edge_map.end() &&
                edge_map.find(edge2) == edge_map.end()) {
                edge_map[edge1] = vertices.size();
                edge_map[edge2] = vertices.size();
                const auto &v1 = _vertices[p1], &v2 = _vertices[p2];
                vertices.push_back(v1 + (v2 - v1) / 2.0);
            }
        };
        for (auto &face : _faces) {
            add_edge(face.a, face.b);
            add_edge(face.b, face.c);
            add_edge(face.c, face.a);
        }

        // Add new faces.
        for (auto &face : _faces) {
            auto &[vi, vj, vk] = face;
            auto e1 = edge_map[{vi, vj}];
            auto e2 = edge_map[{vj, vk}];
            auto e3 = edge_map[{vk, vi}];
            faces.push_back({vi, e1, e3});
            faces.push_back({vj, e2, e1});
            faces.push_back({vk, e3, e2});
            faces.push_back({e1, e2, e3});
        }
    } else {
        // Add center point of each face as an additional vertex.
        for (auto &face : _faces) {
            auto &[vi, vj, vk] = face;
            auto center = (_vertices[vi] + _vertices[vj] + _vertices[vk]) / 3.0;
            vertices.push_back(center);
        }

        // Add new faces.
        size_t i = 0;
        for (auto &face : _faces) {
            auto &[vi, vj, vk] = face;
            auto center = _vertices.size() + i++;
            faces.push_back({vi, center, vk});
            faces.push_back({vj, center, vi});
            faces.push_back({vk, center, vj});
        }
    }

    return {vertices, faces};
}

trimesh_2d_t trimesh_2d_t::make_delaunay() const {
    // Progressively flips edges to make the mesh Delaunay.

    face_list_t faces = _faces;

    // Map from each edge to the associated face.
    edge_map_t<size_t> edge_to_face;
    for (size_t i = 0; i < faces.size(); i++) {
        const auto &face = faces[i];
        for (const auto &edge : face.get_edges(true)) {
            if (edge_to_face.find(edge) != edge_to_face.end()) {
                throw std::runtime_error("Mesh is not manifold.");
            }
            edge_to_face[edge] = i;
        }
    }

    // Visit each edge and check if it needs to be flipped.
    edge_set_t edges;
    std::queue<edge_t> queue;
    edge_set_t in_queue;
    for (auto &[edge, face] : edge_to_face) {
        edges.insert(edge);
        queue.push(edge);
        in_queue.insert(edge);
    }
    while (!queue.empty()) {
        auto &edge = queue.front();
        queue.pop();
        in_queue.erase(edge);
        auto rev_edge = edge.flip();
        if (edge_to_face.find(rev_edge) == edge_to_face.end()) continue;
        size_t face_id = edge_to_face[edge],
               rev_face_id = edge_to_face[rev_edge];
        auto &face = faces[face_id], &rev_face = faces[rev_face_id];
        const auto v1 = edge.a, v2 = edge.b, v3 = face.get_other_vertex(edge),
                   v4 = rev_face.get_other_vertex(rev_edge);
        const auto &p1 = _vertices[v1], &p2 = _vertices[v2],
                   &p3 = _vertices[v3], &p4 = _vertices[v4];

        if (!this->get_triangle(face).circumcircle_contains(p4,
                                                            -get_tolerance()))
            continue;

        // Removes old edge and add new edge.
        edges.erase(edge);
        edges.erase(rev_edge);
        edge_t new_edge = {v3, v4, true}, new_rev_edge = new_edge.flip();
        edges.insert(new_edge);
        edges.insert(new_rev_edge);

        // Removes previous edge to face mappings.
        for (const auto &e : face.get_edges(true)) edge_to_face.erase(e);
        for (const auto &e : rev_face.get_edges(true)) edge_to_face.erase(e);

        // Updates the faces.
        face = {v1, v4, v3};
        rev_face = {v2, v3, v4};

        // Adds new edge to face mappings.
        for (const auto &e : face.get_edges(true)) edge_to_face[e] = face_id;
        for (const auto &e : rev_face.get_edges(true))
            edge_to_face[e] = rev_face_id;

        // Adds the other edges of the new faces to the queue.
        for (const auto &e : face.get_edges(true)) {
            if (in_queue.find(e) == in_queue.end()) {
                queue.push(e);
                in_queue.insert(e);
            }
        }
        for (const auto &e : rev_face.get_edges(true)) {
            if (in_queue.find(e) == in_queue.end()) {
                queue.push(e);
                in_queue.insert(e);
            }
        }
    }

    return {this->_vertices, faces};
}

std::string trimesh_2d_t::to_string() const {
    std::stringstream ss;
    ss << "Trimesh2D(" << std::endl;
    ss << "  " << _vertices.size() << " vertices = [" << std::endl;
    size_t i = 0;
    for (auto &vertex : _vertices) {
        ss << "    " << vertex.to_string() << "," << std::endl;
        if (i++ > 10) {
            ss << "    ..." << std::endl;
            break;
        }
    }
    ss << "  ]," << std::endl;
    ss << "  " << _faces.size() << " faces = [" << std::endl;
    i = 0;
    for (auto &face : _faces) {
        ss << "    " << face.to_string() << std::endl;
        if (i++ > 10) {
            ss << "    ..." << std::endl;
            break;
        }
    }
    ss << "  ]" << std::endl;
    ss << ")" << std::endl;
    return ss.str();
}

trimesh_2d_t trimesh_2d_t::operator<<(const affine_2d_t &tf) const {
    std::vector<point_2d_t> vertices;
    face_list_t faces = this->_faces;
    std::transform(this->_vertices.begin(), this->_vertices.end(),
                   std::back_inserter(vertices),
                   [&tf](const point_2d_t &vertex) { return vertex << tf; });
    return {vertices, faces};
}

trimesh_2d_t trimesh_2d_t::operator|(const trimesh_2d_t &other) const {
    return mesh_union(*this, other);
}

trimesh_2d_t trimesh_2d_t::operator&(const trimesh_2d_t &other) const {
    return mesh_intersection(*this, other);
}

trimesh_2d_t trimesh_2d_t::operator-(const trimesh_2d_t &other) const {
    return mesh_difference(*this, other);
}

/* ----------------------- *
 * Additional constructors *
 * ----------------------- */

trimesh_2d_t triangulate(const std::vector<point_2d_t> &points, bool shuffle) {
    // Reference: https://www.youtube.com/watch?v=1TUUevxkvp4

    if (points.size() < 3) {
        throw std::invalid_argument("Not enough points");
    }

    // Super triangle.
    bounding_box_2d_t bb{points};
    double d = std::max(bb.max.x - bb.min.x, bb.max.y - bb.min.y);
    point_2d_t p1 = {bb.min.x - 10 * d, bb.min.y - d};
    point_2d_t p2 = {bb.max.x + 10 * d, bb.min.y - d};
    point_2d_t p3 = {(bb.min.x + bb.max.x) / 2, bb.max.y + 10 * d};
    triangle_2d_t super_triangle{p1, p2, p3};

    // Generates a random permutation of the point indices.
    std::vector<size_t> indices(points.size());
    std::iota(indices.begin(), indices.end(), 0);
    if (shuffle) {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::shuffle(indices.begin(), indices.end(), gen);
    }

    // Triangulation.
    delaunay_split_tree_2d_t tree{super_triangle};
    for (size_t pi : indices) {
        const auto &p = points[pi];
        const size_t i = tree.find_leaf_index(p);
        tree.split_triangle(p, i, true);
    }

    // Don't remove super triangle (for debugging).
    // face_list_t faces;
    // for (const auto i : tree.get_leaf_triangles()) {
    //     const auto face = tree.get_face(i);
    //     faces.push_back(face);
    // }
    // const auto &old_points = tree.get_vertices().get_points();
    // return {old_points, faces, false};

    // Remove super triangle.
    face_list_t faces;
    for (const auto i : tree.get_leaf_triangles()) {
        const auto face = tree.get_face(i);
        if (face.a < 3 || face.b < 3 || face.c < 3) continue;
        faces.push_back({face.a - 3, face.b - 3, face.c - 3});
    }
    const auto &old_points = tree.get_vertices().get_points();
    std::vector<point_2d_t> new_points(old_points.begin() + 3,
                                       old_points.end());
    return {new_points, faces, false};
}

void add_2d_types_modules(py::module &m) {
    // Defines the classes first, so that methods can resolve types
    // correctly.
    auto point_2d = py::class_<point_2d_t>(m, "Point2D");
    auto line_2d = py::class_<line_2d_t>(m, "Line2D");
    auto triangle_2d = py::class_<triangle_2d_t>(m, "Triangle2D");
    auto circle_2d = py::class_<circle_2d_t>(m, "Circle2D");
    auto bbox_2d = py::class_<bounding_box_2d_t>(m, "BoundingBox2D");
    auto polygon_2d = py::class_<polygon_2d_t>(m, "Polygon2D");
    auto affine_2d = py::class_<affine_2d_t>(m, "Affine2D");
    auto trimesh_2d = py::class_<trimesh_2d_t>(m, "Trimesh2D");

    // Defines Point2D methods.
    point_2d
        .def(py::init<double, double>(), "A point in 2D space", "x"_a, "y"_a)
        .def_readwrite("x", &point_2d_t::x, "The point's x coordinate")
        .def_readwrite("y", &point_2d_t::y, "The point's y coordinate")
        .def("__str__", &point_2d_t::to_string, py::is_operator())
        .def("__repr__", &point_2d_t::to_string, py::is_operator())
        .def("__hash__", &point_2d_hash_fn, py::is_operator())
        .def("__add__",
             py::overload_cast<const point_2d_t &, const point_2d_t &>(
                 &operator+),
             "Vector addition with another point", "other"_a, py::is_operator())
        .def("__iadd__", &point_2d_t::operator+=,
             "Vector addition with another point", "other"_a, py::is_operator())
        .def("__sub__",
             py::overload_cast<const point_2d_t &, const point_2d_t &>(
                 &operator-),
             "Vector subtraction with another point", "other"_a,
             py::is_operator())
        .def("__isub__", &point_2d_t::operator-=,
             "Vector subtraction with another point", "other"_a,
             py::is_operator())
        .def("__mul__",
             py::overload_cast<const point_2d_t &, const point_2d_t &>(
                 &operator*),
             "Vector dot product with another point", "other"_a,
             py::is_operator())
        .def("__mul__",
             py::overload_cast<double, const point_2d_t &>(&operator*),
             "Scalar multiplication with a double", "other"_a,
             py::is_operator())
        .def("__mul__",
             py::overload_cast<const point_2d_t &, double>(&operator*),
             "Scalar multiplication with a double", "other"_a,
             py::is_operator())
        .def("__imul__",
             py::overload_cast<const point_2d_t &>(&point_2d_t::operator*=),
             "Vector dot product with another point", "other"_a,
             py::is_operator())
        .def("__imul__", py::overload_cast<double>(&point_2d_t::operator*=),
             "Scalar multiplication with a double", "other"_a,
             py::is_operator())
        .def("__truediv__",
             py::overload_cast<const point_2d_t &, const point_2d_t &>(
                 &operator/),
             "Vector division with another point", "other"_a, py::is_operator())
        .def("__truediv__",
             py::overload_cast<const point_2d_t &, double>(&operator/),
             "Scalar division with a double", "other"_a, py::is_operator())
        .def("__itruediv__",
             py::overload_cast<const point_2d_t &>(&point_2d_t::operator/=),
             "Vector division with another point", "other"_a, py::is_operator())
        .def("__itruediv__", py::overload_cast<double>(&point_2d_t::operator/=),
             "Scalar division with a double", "other"_a, py::is_operator())
        .def("__eq__", &point_2d_t::operator==, "Equality with another point",
             "other"_a, py::is_operator())
        .def("__ne__", &point_2d_t::operator!=, "Inequality with another point",
             "other"_a, py::is_operator())
        .def("__lt__", &point_2d_t::operator<, "Less than another point",
             "other"_a, py::is_operator())
        .def("__lshift__",
             py::overload_cast<const point_2d_t &, const affine_2d_t &>(
                 &operator<<),
             "Stream insertion operator for a point", "other"_a,
             py::is_operator())
        .def("__ilshift__", &point_2d_t::operator<<=,
             "Stream insertion operator for a point", "other"_a,
             py::is_operator())
        .def("normalize", &point_2d_t::normalize, "Normalize by length")
        .def("rotate", &point_2d_t::rotate,
             "Rotate around (0, 0) by some angle", "angle"_a)
        .def("determinant", &point_2d_t::determinant,
             "Determinant of a 2x2 matrix with another point", "other"_a)
        .def("length", &point_2d_t::length, "Vector length")
        .def("dot", &point_2d_t::dot, "Dot product with another point",
             "other"_a)
        .def("cross", &point_2d_t::cross, "Cross product with another point",
             "other"_a)
        .def("angle", &point_2d_t::angle, "Angle between two vectors",
             "other"_a)
        .def("barycentric_coordinates", &point_2d_t::barycentric_coordinates,
             "Barycentric coordinates of a point in a triangle", "t"_a)
        .def("is_inside_triangle", &point_2d_t::is_inside_triangle,
             "Is inside a triangle", "t"_a)
        .def("is_inside_bounding_box", &point_2d_t::is_inside_bounding_box,
             "Is inside a bounding box", "bb"_a)
        .def("distance_to_point", &point_2d_t::distance_to_point,
             "Distance to another point", "p"_a)
        .def("distance_to_line", &point_2d_t::distance_to_line,
             "Distance to a line", "l"_a)
        .def("distance_to_triangle", &point_2d_t::distance_to_triangle,
             "Distance to a triangle", "t"_a)
        .def("distance_to_bounding_box", &point_2d_t::distance_to_bounding_box,
             "Distance to a bounding box", "bb"_a)
        .def("project_to_line", &point_2d_t::project_to_line,
             "Project onto a line", "other"_a);

    // Defines Line2D methods.
    line_2d
        .def(py::init<const point_2d_t &, const point_2d_t &>(),
             "A line in 2D space", "p1"_a, "p2"_a)
        .def_readwrite("p1", &line_2d_t::p1, "The line's first point")
        .def_readwrite("p2", &line_2d_t::p2, "The line's second point")
        .def("__str__", &line_2d_t::to_string, py::is_operator())
        .def("__repr__", &line_2d_t::to_string, py::is_operator())
        .def("__eq__", &line_2d_t::operator==, "Equality with another line",
             "other"_a, py::is_operator())
        .def("__ne__", &line_2d_t::operator!=, "Inequality with another line",
             "other"_a, py::is_operator())
        .def("__lt__", &line_2d_t::operator<, "other"_a, py::is_operator())
        .def("__lshift__",
             py::overload_cast<const line_2d_t &, const affine_2d_t &>(
                 &operator<<),
             "Applies a affine transformation to the line", "other"_a,
             py::is_operator())
        .def("__ilshift__", &line_2d_t::operator<<=,
             "Applies a affine transformation to the line", "other"_a,
             py::is_operator())
        .def("closest_point", &line_2d_t::closest_point,
             "The closest point on the line to another point", "p"_a)
        .def("line_intersection", &line_2d_t::line_intersection,
             "The intersection point of two lines (None if they don't "
             "intersect)",
             "l"_a)
        .def("intersects_triangle", &line_2d_t::intersects_triangle,
             "Does the line intersect a triangle", "t"_a)
        .def("intersects_bounding_box", &line_2d_t::intersects_bounding_box,
             "Does the line intersect a bounding box", "bb"_a)
        .def("distance_to_point", &line_2d_t::distance_to_point,
             "Distance to a point", "p"_a)
        .def("distance_to_line", &line_2d_t::distance_to_line,
             "Distance to another line", "l"_a)
        .def("distance_to_triangle", &line_2d_t::distance_to_triangle,
             "Distance to a triangle", "t"_a)
        .def("distance_to_bounding_box", &line_2d_t::distance_to_bounding_box,
             "Distance to a bounding box", "bb"_a);

    // Defines Triangle2D methods.
    triangle_2d
        .def(py::init<const point_2d_t &, const point_2d_t &,
                      const point_2d_t &>(),
             "A triangle in 2D space", "p1"_a, "p2"_a, "p3"_a)
        .def_readwrite("p1", &triangle_2d_t::p1, "The triangle's first point")
        .def_readwrite("p2", &triangle_2d_t::p2, "The triangle's second point")
        .def_readwrite("p3", &triangle_2d_t::p3, "The triangle's third point")
        .def("__str__", &triangle_2d_t::to_string, py::is_operator())
        .def("__repr__", &triangle_2d_t::to_string, py::is_operator())
        .def("__eq__", &triangle_2d_t::operator==,
             "Equality with another triangle", "other"_a, py::is_operator())
        .def("__ne__", &triangle_2d_t::operator!=,
             "Inequality with another triangle", "other"_a, py::is_operator())
        .def("__lt__", &triangle_2d_t::operator<, "other"_a, py::is_operator())
        .def("__lshift__",
             py::overload_cast<const triangle_2d_t &, const affine_2d_t &>(
                 &operator<<),
             "Applies a affine transformation to the triangle", "other"_a,
             py::is_operator())
        .def("__ilshift__", &triangle_2d_t::operator<<=,
             "Applies a affine transformation to the triangle", "other"_a,
             py::is_operator())
        .def("area", &triangle_2d_t::area, "The triangle's area")
        .def("center", &triangle_2d_t::center, "The triangle's center")
        .def("vertices", &triangle_2d_t::vertices, "The triangle's vertices")
        .def("edges", &triangle_2d_t::edges, "The triangle's edges")
        .def("is_clockwise", &triangle_2d_t::is_clockwise,
             "Is the triangle clockwise")
        .def("circumcircle", &triangle_2d_t::circumcircle,
             "The triangle's circumscribed circle")
        .def("circumcircle_contains", &triangle_2d_t::circumcircle_contains,
             "Is the point inside the circumcircle of the triangle", "p"_a,
             "tolerance"_a = 0.0)
        .def("contains_point", &triangle_2d_t::contains_point,
             "Does the triangle contain a point", "p"_a)
        .def("contains_triangle", &triangle_2d_t::contains_triangle,
             "Does the triangle contain another triangle", "t"_a)
        .def("intersects_bounding_box", &triangle_2d_t::intersects_bounding_box,
             "Does the triangle intersect a bounding box", "bb"_a)
        .def("intersects_triangle", &triangle_2d_t::intersects_triangle,
             "Does the triangle intersect another triangle", "t"_a)
        .def("distance_to_point", &triangle_2d_t::distance_to_point,
             "Distance to a point", "p"_a)
        .def("distance_to_line", &triangle_2d_t::distance_to_line,
             "Distance to a line", "l"_a)
        .def("distance_to_triangle", &triangle_2d_t::distance_to_triangle,
             "Distance to another triangle", "t"_a)
        .def("distance_to_bounding_box",
             &triangle_2d_t::distance_to_bounding_box,
             "Distance to a bounding box", "bb"_a)
        .def("point_from_barycentric_coords",
             &triangle_2d_t::point_from_barycentric_coords,
             "Returns a point from barycentric coordinates", "b"_a);

    // Defines Circle2D methods.
    circle_2d
        .def(py::init<const point_2d_t &, double>(), "A circle in 2D space",
             "center"_a, "radius"_a)
        .def(py::init<const triangle_2d_t>(), "The circumcircle of a triangle",
             "triangle"_a)
        .def_readwrite("center", &circle_2d_t::center, "The circle's center")
        .def_readwrite("radius", &circle_2d_t::radius, "The circle's radius")
        .def_property_readonly("area", &circle_2d_t::area, "The circle's area")
        .def_property_readonly("circumference", &circle_2d_t::circumference,
                               "The circle's circumference")
        .def("__str__", &circle_2d_t::to_string, py::is_operator())
        .def("__repr__", &circle_2d_t::to_string, py::is_operator())
        .def("__eq__", &circle_2d_t::operator==, "Equality with another circle",
             "other"_a, py::is_operator())
        .def("__ne__", &circle_2d_t::operator!=,
             "Inequality with another circle", "other"_a, py::is_operator())
        .def("contains_point", &circle_2d_t::contains_point,
             "Does the circle contain a point", "p"_a, "tolerance"_a = 0.0)
        .def("intersection", &circle_2d_t::intersection,
             "The intersection of two circles", "other"_a);

    // Defines BoundingBox2D methods.
    bbox_2d
        .def(py::init<const point_2d_t &, const point_2d_t &>(),
             "Creates a bounding box from two points", "min"_a, "max"_a)
        .def(py::init<const std::vector<point_2d_t> &>(),
             "Creates a bounding box from a list of points", "points"_a)
        .def(py::init<const std::vector<line_2d_t> &>(),
             "Creates a bounding box from a list of lines", "lines"_a)
        .def(py::init<const std::vector<triangle_2d_t> &>(),
             "Creates a bounding box from a list of triangles", "triangles"_a)
        .def(py::init<const std::vector<bounding_box_2d_t> &>(),
             "Creates a bounding box from a list of other bounding boxes",
             "bboxes"_a)
        .def_readwrite("min", &bounding_box_2d_t::min,
                       "The bounding box's minimum point")
        .def_readwrite("max", &bounding_box_2d_t::max,
                       "The bounding box's maximum point")
        .def("__str__", &bounding_box_2d_t::to_string, py::is_operator())
        .def("__repr__", &bounding_box_2d_t::to_string, py::is_operator())
        .def("__eq__", &bounding_box_2d_t::operator==,
             "Equality with another bounding box", "other"_a, py::is_operator())
        .def("__ne__", &bounding_box_2d_t::operator!=,
             "Inequality with another bounding box", "other"_a,
             py::is_operator())
        .def("__lshift__",
             py::overload_cast<const bounding_box_2d_t &, const affine_2d_t &>(
                 &operator<<),
             "Applies a affine transformation to the bounding box", "other"_a,
             py::is_operator())
        .def("__ilshift__", &bounding_box_2d_t::operator<<=,
             "Applies a affine transformation to the bounding box", "other"_a,
             py::is_operator())
        .def("area", &bounding_box_2d_t::area, "The bounding box's area")
        .def("center", &bounding_box_2d_t::center, "The bounding box's center")
        .def("vertices", &bounding_box_2d_t::vertices,
             "The bounding box's vertices")
        .def("edges", &bounding_box_2d_t::edges, "The bounding box's edges")
        .def("intersects_triangle", &bounding_box_2d_t::intersects_triangle,
             "Does the bounding box intersect a triangle", "t"_a)
        .def("contains_point", &bounding_box_2d_t::contains_point,
             "Does the bounding box contain a point", "p"_a)
        .def("contains_triangle", &bounding_box_2d_t::contains_triangle,
             "Does the bounding box contain a triangle", "t"_a)
        .def("distance_to_point", &bounding_box_2d_t::distance_to_point,
             "Distance to a point", "p"_a)
        .def("distance_to_line", &bounding_box_2d_t::distance_to_line,
             "Distance to a line", "l"_a)
        .def("distance_to_triangle", &bounding_box_2d_t::distance_to_triangle,
             "Distance to a triangle", "t"_a)
        .def("distance_to_bounding_box",
             &bounding_box_2d_t::distance_to_bounding_box,
             "Distance to another bounding box", "bb"_a);

    // Defines Polygon2D methods.
    polygon_2d
        .def(py::init<const std::vector<point_2d_t> &>(),
             "Creates a polygon from a list of points", "points"_a)
        .def_readwrite("points", &polygon_2d_t::points,
                       "The polygon's list of points")
        .def("__str__", &polygon_2d_t::to_string, py::is_operator())
        .def("__repr__", &polygon_2d_t::to_string, py::is_operator())
        .def("__eq__", &polygon_2d_t::operator==,
             "Equality with another polygon", "other"_a, py::is_operator())
        .def("__ne__", &polygon_2d_t::operator!=,
             "Inequality with another polygon", "other"_a, py::is_operator())
        .def("__lshift__",
             py::overload_cast<const polygon_2d_t &, const affine_2d_t &>(
                 &operator<<),
             "Applies a affine transformation to the polygon", "other"_a,
             py::is_operator())
        .def("__ilshift__", &polygon_2d_t::operator<<=,
             "Applies a affine transformation to the polygon", "other"_a,
             py::is_operator())
        .def("__add__", &polygon_2d_t::operator+, "Concatenates two polygons",
             "other"_a, py::is_operator())
        .def("__iadd__", &polygon_2d_t::operator+=, "Concatenates two polygons",
             "other"_a, py::is_operator())
        .def("signed_area", &polygon_2d_t::signed_area,
             "The polygon's signed area (positive if counterclockwise)")
        .def("is_clockwise", &polygon_2d_t::is_clockwise,
             "Returns true if the polygon is clockwise")
        .def("reverse", &polygon_2d_t::reverse, "Reverses the polygon's points")
        .def("convex_hull", &polygon_2d_t::convex_hull,
             "Returns the polygon's convex hull")
        .def("bounding_box", &polygon_2d_t::bounding_box,
             "Returns the polygon's bounding box")
        .def("center", &polygon_2d_t::center, "Returns the polygon's center")
        .def("get_trimesh", &polygon_2d_t::get_trimesh,
             "Returns a triangle mesh representation of the polygon. Set "
             "`is_convex` to True if the polygon is definitely convex; this "
             "will speed up the computation",
             "delaunay"_a = false, "is_convex"_a = false);

    // Defines Affine2D methods.
    affine_2d
        .def(py::init<std::tuple<std::tuple<double, double>,
                                 std::tuple<double, double>>,
                      std::tuple<double, double>>(),
             "Creates an affine transformation from a 2x2 matrix and a 2x1 "
             "translation vector",
             "matrix"_a, "translation"_a)
        .def(py::init<std::optional<double>,
                      std::optional<std::tuple<double, double>>,
                      std::optional<double>>(),
             "Initialize affine transformation from rotation and "
             "translation "
             "vectors",
             "rot"_a = std::nullopt, "trans"_a = std::nullopt,
             "scale"_a = std::nullopt)
        .def("__str__", &affine_2d_t::to_string, py::is_operator())
        .def("__repr__", &affine_2d_t::to_string, py::is_operator())
        .def("__matmul__",
             py::overload_cast<const affine_2d_t &, const affine_2d_t &>(
                 &operator*),
             "Combine two affine transformations", "other"_a, py::is_operator())
        .def("__imatmul__", &affine_2d_t::operator*=,
             "Applies an affine transformation to a point", "other"_a,
             py::is_operator())
        .def("__rshift__",
             py::overload_cast<const affine_2d_t &, const point_2d_t &>(
                 &operator>>),
             "Applies an affine transformation to a point", "other"_a,
             py::is_operator())
        .def("__rshift__",
             py::overload_cast<const affine_2d_t &, const line_2d_t &>(
                 &operator>>),
             "Applies an affine transformation to a line", "other"_a,
             py::is_operator())
        .def("__rshift__",
             py::overload_cast<const affine_2d_t &, const triangle_2d_t &>(
                 &operator>>),
             "Applies an affine transformation to a triangle", "other"_a,
             py::is_operator())
        .def("__rshift__",
             py::overload_cast<const affine_2d_t &, const bounding_box_2d_t &>(
                 &operator>>),
             "Applies an affine transformation to a bounding box", "other"_a,
             py::is_operator())
        .def("__rshift__",
             py::overload_cast<const affine_2d_t &, const polygon_2d_t &>(
                 &operator>>),
             "Applies an affine transformation to a polygon", "other"_a,
             py::is_operator())
        .def("inverse", &affine_2d_t::inverse,
             "The inverse of the affine transformation")
        .def_property_readonly("rotation", &affine_2d_t::rotation,
                               "The affine transformation's rotation matrix")
        .def_property_readonly(
            "translation", &affine_2d_t::translation,
            "The affine transformation's translation vector");

    // Defines Trimesh2D methods.
    trimesh_2d
        // .def(py::init<const std::vector<point_2d_t> &, const face_set_t &,
        //               bool>(),
        //      "Creates a trimesh from vertices and faces", "vertices"_a,
        //      "faces"_a, "validate"_a = false)
        // .def(py::init<const std::vector<point_2d_t> &, const face_list_t &,
        //               bool>(),
        //      "Creates a trimesh from vertices and faces", "vertices"_a,
        //      "faces"_a, "validate"_a = false)
        .def_property_readonly("vertices", &trimesh_2d_t::vertices,
                               "The mesh vertices")
        .def_property_readonly("faces", &trimesh_2d_t::faces, "The mesh faces")
        .def("get_triangle", &trimesh_2d_t::get_triangle,
             "Returns the triangle for a given face", "face"_a)
        .def("get_triangles", &trimesh_2d_t::get_triangles,
             "Returns all the triangles in the trimesh")
        .def("get_polygons", &trimesh_2d_t::get_polygons,
             "Returns the polygon inscribing the trimesh")
        .def("subdivide", &trimesh_2d_t::subdivide,
             "Splits each triangle into four smaller triangles",
             "at_edges"_a = true)
        .def("make_delaunay", &trimesh_2d_t::make_delaunay,
             "Creates a Delaunay triangulation of the mesh")
        .def("union", &trimesh_2d_t::operator|,
             "Computes the union of two 2D meshes", "other"_a)
        .def("intersection", &trimesh_2d_t::operator&,
             "Computes the intersection of two 2D meshes", "other"_a)
        .def("difference", &trimesh_2d_t::operator-,
             "Computes the difference of two 2D meshes", "other"_a)
        .def("__str__", &trimesh_2d_t::to_string, py::is_operator())
        .def("__repr__", &trimesh_2d_t::to_string, py::is_operator())
        .def("__or__", &trimesh_2d_t::operator|,
             "Computes the union of two 2D meshes", "other"_a,
             py::is_operator())
        .def("__and__", &trimesh_2d_t::operator&,
             "Computes the intersection of two 2D meshes", "other"_a,
             py::is_operator())
        .def("__sub__", &trimesh_2d_t::operator-,
             "Computes the difference of two 2D meshes", "other"_a,
             py::is_operator())
        .def("__lshift__", &trimesh_2d_t::operator<<,
             "Applies affine transformation to the mesh", "affine"_a,
             py::is_operator());

    // Defines additional constructors.
    m.def("triangulate_2d", &triangulate, "Triangulates a set of points",
          "polygon"_a, "shuffle"_a = true);
}

}  // namespace trimesh
