from scipy.stats import skewnorm
from scipy.stats import foldnorm
from scipy.stats import poisson
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt

def get_beta_given_mode(a, mode):
        beta = (a-1)/mode -a +2
        return beta

def pdf_multimodal_beta_array(x, a1,b1,a2,b2, epsilon):
        scale_x = 1/epsilon
        composition = beta.pdf(x * scale_x, a1, b1)+ beta.pdf(x * scale_x, a2, b2)
        scale_y = max(composition)
        # Normalize so maximum value is 1
        composition = composition/scale_y
        return composition, scale_x, scale_y

def multimodal_beta_single_value(x, a1,b1,a2,b2, scale_x, scale_y):
        beta_distr_value = (beta.pdf(x * scale_x, a1, b1)+ beta.pdf(x * scale_x, a2, b2)) / scale_y
        return beta_distr_value

def compute_average_degree(pdf, N, x, epsilon, mode_3D):
        #scale_x = epsilon
        #dr = 1/(len(x)) *scale_x
        #print(f"lenx {len(x)}")
        dr = (1/len(x))*epsilon
        a = 2  # regular value 3.5

        if mode_3D:
                degree_density = 3*a*N*(x**2)*dr    # If you integrate this, you get the average the degree for epsilon-ball graph
        else:
                degree_density = 2 * a * N * x * dr

        average_degree_epsilon = np.sum(degree_density*np.ones(len(x))) # This is the integration
        #print("average_degree_epsilon-ball", average_degree_epsilon)

        average_degree = np.sum(degree_density*pdf)   # Integration weighted with the current pdf
        # print(degree_density*pdf)
        #print("predicted average_degree", average_degree)
        return average_degree


def pdf_weibull_distribution(parameter_k, parameter_lambda, x, epsilon):
        scale_x = 1/epsilon
        x = x*scale_x
        ini_factor = (parameter_k/parameter_lambda)*np.power((x/parameter_lambda),parameter_k-1)

        exp_factor = np.exp(-np.power(x/parameter_lambda, parameter_k))

        array_pdf = ini_factor * exp_factor
        scale_y = np.amax(array_pdf)
        weibull_dist = array_pdf/scale_y
        return weibull_dist, scale_x, scale_y

def weibull_distribution_single_value(parameter_k, parameter_lambda, x, scale_x, scale_y):
        x = x*scale_x
        ini_factor = (parameter_k/parameter_lambda)*np.power((x/parameter_lambda),parameter_k-1)
        exp_factor = np.exp(-np.power(x/parameter_lambda, parameter_k))

        return (ini_factor*exp_factor) / scale_y

# # OLD VERSION THAT WAS NOT COMPUTING DEGREE TOO WELL
# def get_pdf_parameters_desired_degree_beta_multimodal(desired_degree, epsilon_range, N, x, a1,b1,a2,b2):
#         """
#         For the beta multimodal distribution.
#         Given a desired degree find:
#                 scale_x --> x*scale_x so x_max is epsilon (the cut-off for the graph)
#                 scale_y --> pdf / scale_y  so max(pdf) is 1
#                 epsilon --> The distance cut-off in order to have the desired degree
#                 composition --> the pdf discretized in a numpy array
#         """
#         for epsilon in np.linspace(0.0001, epsilon_range, 1000):
#                 composition, scale_x, scale_y = pdf_multimodal_beta_array(x,a1,b1,a2,b2, epsilon)
#                 average_degree = compute_average_degree(composition, N, x, epsilon)
#                 if desired_degree < average_degree < desired_degree+2:
#                         print(f"Epsilon found: {epsilon}. Average degree: {average_degree}")
#                         break
#
#         else:
#                 raise ValueError(f"Could not find the desired degree: {desired_degree}."
#                                  f"\nSuggestions:\na) Try changing the pdf parameters\nb) Increase the range for epsilon")
#         return epsilon, scale_x, scale_y, composition


def get_pdf_parameters_desired_degree_beta_multimodal(desired_degree, epsilon_range, N, x, a1, b1, a2, b2, mode_3D):
        """
        For the beta multimodal distribution.
        Given a desired degree find:
                scale_x --> x*scale_x so x_max is epsilon (the cut-off for the graph)
                scale_y --> pdf / scale_y  so max(pdf) is 1
                epsilon --> The distance cut-off in order to have the desired degree
                composition --> the pdf discretized in a numpy array
        """
        initial_x = x
        for epsilon in np.linspace(0.0001, epsilon_range, 1000):
                composition, scale_x, scale_y = pdf_multimodal_beta_array(initial_x,a1,b1,a2,b2, epsilon)
                scaled_x = initial_x*epsilon   # Values that go from 0 to epsilon, not from 0 to 1
                pdf_till_epsilon = multimodal_beta_single_value(scaled_x,a1,b1,a2,b2,scale_x,scale_y)  # pdf evaluated for 0 to epsilon points
                average_degree = compute_average_degree(pdf_till_epsilon, N, scaled_x, epsilon, mode_3D)
                if desired_degree < average_degree < desired_degree+2:
                        print(f"Epsilon found: {epsilon}. Average degree: {average_degree}")
                        # Increase epsilon to ensure av degree is sufficient
                        epsilon += 0.05
                        composition, scale_x, scale_y = pdf_multimodal_beta_array(initial_x, a1, b1, a2, b2, epsilon)
                        break

        else:
                raise ValueError(f"Could not find the desired degree: {desired_degree}."
                                 f"\nSuggestions:\na) Try changing the pdf parameters\nb) Increase the range for epsilon")
        return epsilon, scale_x, scale_y, composition

def get_pdf_parameters_desired_degree_weibull(desired_degree, epsilon_range, N, x, parameter_k, parameter_lambda, mode_3D):
        """
        For the weibull distribution.
        Given a desired degree find:
                scale_x --> x*scale_x so x_max is epsilon (the cut-off for the graph)
                scale_y --> pdf / scale_y  so max(pdf) is 1
                epsilon --> The distance cut-off in order to have the desired degree
                composition --> the pdf discretized in a numpy array
        """
        initial_x = x
        for epsilon in np.linspace(0.0001, epsilon_range, 1000):
                composition, scale_x, scale_y = pdf_weibull_distribution(parameter_k, parameter_lambda, initial_x, epsilon)
                scaled_x = initial_x*epsilon   # Values that go from 0 to epsilon, not from 0 to 1
                pdf_till_epsilon = weibull_distribution_single_value(parameter_k, parameter_lambda, scaled_x, scale_x, scale_y)  # pdf evaluated for 0 to epsilon points

                average_degree = compute_average_degree(pdf_till_epsilon, N, scaled_x, epsilon, mode_3D)
                if desired_degree < average_degree < desired_degree+2:
                        #print(f"Epsilon found: {epsilon}")


                        # fig = plt.figure()
                        # ax = fig.add_subplot(111)
                        # print(f"scale_x {scale_x}, scale_y {scale_y}, epsilon {epsilon}")
                        # ax.plot(x, pdf_till_epsilon,
                        #         'r-', lw=5, alpha=0.6, label='skewnorm pdf')

                        break

        else:
                raise ValueError(f"Could not find the desired degree: {desired_degree}."
                                 f"\nSuggestions:\na) Try changing the pdf parameters\nb) Increase the range for epsilon")
        return epsilon, scale_x, scale_y, composition


# # Run this to play with random proximity graphs

# a1,a2 = 5, 5
# mode1, mode2 = 0.3, 0.9 # In a 0,1 interval
# b1,b2 = get_beta_given_mode(a1, mode1), get_beta_given_mode(a2, mode2)
#
# parameter_k = 1.2
# parameter_lambda = 0.8
#
# print(b1,b2)
# # epsilon = 0.3
# N = 1000
# x = np.linspace(0, 1, 10000)
# desired_degree = 15
# epsilon_range = 1
#
# # Weibull
# epsilon, scale_x, scale_y, composition = get_pdf_parameters_desired_degree_weibull(desired_degree, epsilon_range, N, x, parameter_k, parameter_lambda)
#
# # Beta multimodal
# #epsilon, scale_x, scale_y, composition = get_pdf_parameters_desired_degree_beta_multimodal(desired_degree, epsilon_range, N, x, a1,b1,a2,b2)
# value_pdf = weibull_distribution_single_value(parameter_k, parameter_lambda, 0.1, scale_x, scale_y)
#
# print(f'value_pdf {value_pdf}')
#
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
#
# print(f"scale_x {scale_x}, scale_y {scale_y}, epsilon {epsilon}")
# ax.plot(x, composition,
#          'r-', lw=5, alpha=0.6, label='skewnorm pdf')
# # ax.plot(x, beta.pdf(x*scale_x, a, b, loc=loc, scale=scale)/scale_y,
# #         'r-', lw=5, alpha=0.6, label='skewnorm pdf')
# plt.show()
# # ax.plot(x, skewnorm.pdf(x, a, loc=loc, scale=scale),
# #        'r-', lw=5, alpha=0.6, label='skewnorm pdf')

