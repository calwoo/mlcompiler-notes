#include <iostream>
#include <cmath>
#include <random>


double pi_mc_approx(int num_throws) {
    int count_in = 0;
    double x, y, d;

    for (auto i = 0; i < num_throws; i++) {
        x = static_cast<double>(rand()) / RAND_MAX;
        y = static_cast<double>(rand()) / RAND_MAX;
        d = sqrt(pow(x, 2) + pow(y, 2));
        if (d < 1.0)
            count_in++;
    }

    // compute pi
    double frac_quadrant = static_cast<double>(count_in) / num_throws;
    return 4.0 * (frac_quadrant);
}

int main() {
    int num_throws = 5000000;
    std::cout << pi_mc_approx(num_throws) << std::endl;
    return 0;
}
