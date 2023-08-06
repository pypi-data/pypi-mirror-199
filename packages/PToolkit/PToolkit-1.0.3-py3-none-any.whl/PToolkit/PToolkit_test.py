import numpy as np


def Round_sigfig(x, fig, type_rounding="Normal", format="numerical", debug=False):
    """
    Function to round a number (or array) to n significant digits


    Input:
        x (float): a number that needs to be rounded 
        fig (int): the number of significant digits
        type (str): the type of rounding
            "Normal": rounds to the closest number
            "Up": rounds up
            "Down": rounds down
        format (str): the data type it should return

    Output:
        (float/int) a number rounded based on the amount of significant digits

    """
    # Define a result variable
    result = None

    # Determine the highest power of 10 that can fit in x
    int_count_10 = np.floor(np.log10(np.abs(x)))

    # Use normal rounding
    if type_rounding == "Normal":
        
        # Determine the shifting factor
        shifter = 10**int_count_10

        # Shift x by shifter round n digits and shift x back by shifter
        result = np.round(x / shifter, fig-1)*shifter
    
    # Use ceil to round
    elif type_rounding == "Up":

        # Determine the shifting factor
        shifter = 10**(fig - int_count_10 - 1)

        # Shift x by shifter round n digits up and shift x back by shifter
        result = np.ceil(x * shifter)/shifter

    # Use floor to round
    elif type_rounding == "Down":

        # Determine the shifting factor
        shifter = 10**(fig - int_count_10 - 1)

        # Shift x by shifter round n digits down and shift x back by shifter
        result = np.floor(x * shifter)/shifter

    else:
        raise ValueError("Unkown type of rounding only Normal, Up and Down are available")

    final_result = result

    # Post proces values to text
    if format == "text":

        if debug:
            print(f"==========Text proccessing==========")

        final_result = []

        # Loop over the results
        for i in result:
            i = str(i)
            
            if debug:
                print(f"Given value: {i}")


            if "e" in i:
                raise ValueError("No support for formats with e")

            # Remove the .  
            i_raw = i.replace(".", "")

            # Split i
            i_split = i.split(".")
            before = i_split[0]
            after = i_split[1]

            # Check if there are useless 0 in i if so remove them
            if before == "0":
                i_raw = i.replace(".", "").lstrip("0")

            # Check if useless zero on the end of i if so remove it
            if len(i_raw) > fig:
                if after == "0":
                    i = before

            # Add extra zero if the amount of fig is not satistifed. 
            elif len(i_raw) < fig:
                i += "0"*(fig-len(i_raw))

            if debug:
                print(f"Value changed to: {i}\n")            

            final_result.append(i)
    final_result = np.array(final_result)

    
                       
    return final_result



from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt


def Fourier_series_cos_term(func, k, omega_0):
    """
    Decorator to convert any function to a intergrant for a fourier series (cos)

    Input:
        func (python function object): A function that needs te be converted
        k (int): The index of the fourier sereies
        omega_0 (float): The ground radial velocity

    Output:
        A function multiplied by the cosine term in a fourier series 
    """

    # Create a wrapper and take all arguments from the function
    def wrapper(*args, **kwargs):
        # Convert  the function by passing all arguments in to the function 
        # Then multipli the function by cosine and give it as input the 
        # The index multiplied by the ground radial velocity and t (args[0] must be the variable)
        result = func(*args, **kwargs)*np.cos(k*omega_0*args[0])

        # Return the result of the function
        return result

    # Return the wrapper as the new function
    return wrapper


def Fourier_series_sin_term(func, k, omega_0):
    """
    Decorator to convert any function to a intergrant for a fourier series (sin)

    Input:
        func (python function object): A function that needs te be converted
        k (int): The index of the fourier sereies
        omega_0 (float): The ground radial velocity

    Output:
        A function multiplied by the sine term in a fourier series 
    """

    # Create a wrapper and take all arguments from the function
    def wrapper(*args, **kwargs):
        # Convert  the function by passing all arguments in to the function 
        # Then multipli the function by cosine and give it as input the 
        # The index multiplied by the ground radial velocity and t (args[0] must be the variable)
        result = func(*args, **kwargs)*np.sin(k*omega_0*args[0])

        # Return the result of the function
        return result

    # Return the wrapper as the new function
    return wrapper


def Fourier_series_func(a_0, a_n, b_n, T):
    """
    A function when given the coefficients of a fourier series it wil return a python function that describes the 
    fourier series that is described with the those coefficients.

    Input:
        a_0 (float): DC level of the signal
        a_n (float): The coefficient infront of the cos term
        b_n (float): The coefficient infront of the sin term
    """
    
    # Create a wrapper
    def wrapper(x):

        # Create a result variable and set it equal to the DC level
        result = a_0

        # Start looping over de coefficients
        for k in range(0, len(a_n)):

            # Add each term of the fourier series to the result variable. 
            result += a_n[k]*np.cos(((k+1)*2*np.pi*x)/T) + b_n[k]*np.sin(((k+1)*2*np.pi*x)/T)

        # Return the result variable
        return result

    # Return the wrapper
    return wrapper


def Real_fourier_series(func, T, n):
    """
    A function to calculate the coefficients of the fourier series for any function numerically
    Input:
        func (python function object): The function of which the fourier series has te be
            calculated
        T (float): The period of the 
        n (int): the amount of terms of the fourier series
    """

    # Calculate the ground radial velocity
    omega_0 = 2*np.pi/T

    # Create arrays for the coefficients of the fourier series
    array_a_n = []
    array_b_n = []

    # Calculate a_0 of the fourier series
    a_0 = 1/T*quad(func, -T/2, T/2)[0]

    # Loop over the terms
    for k in range(1, n):

        # Convert the function given to the intergrand for the value k
        func_cos = Fourier_series_cos_term(func, omega_0, k)
        func_sin = Fourier_series_sin_term(func, omega_0, k)

        # Calculate the intergral using scipy 
        a_n = 2/T*quad(func_cos, -T/2, T/2)[0]
        b_n = 2/T*quad(func_sin, -T/2, T/2)[0]

        # Append the coefficients to there respected arrays
        array_a_n.append(a_n)
        array_b_n.append(b_n)

    # Return a_0 and the coefficient arrays
    return a_0, array_a_n, array_b_n
    
def Fourier_series(func, T, n, algorithm="real"):
    """
    A function that wil calculate the fourier series of any signal described by a python function

    Input:
        func (python function): A python function that describes a mathmetical function.
        T (float): The period of signal.
        n (int): The amount of terms of the fourier series
        algorithm (str): 'real' or 'complex' 
    """
    
    # Check if the algorithm is the real fourier series
    if algorithm == "real":

        # Calculate the coefficients of the fourier series
        a_0, a_n, b_n = Real_fourier_series(func, T, n)

    # Check if the algorithm is the complex fourier series
    elif algorithm == "complex":
        raise NotImplementedError("This feature is not implemented")

    else:
        raise NameError("Unknown algorithm")

    # Return the python function that describes the fourier series of the signal.
    return Fourier_series_func(a_0, a_n, b_n, T)

def Fourier_series_exp_term(func, k, T):
    def wrapper(*args, **kwargs):
        exponent = 0 + -((k*np.pi)/T)*1j
        result = func(*args, **kwargs)*np.exp(exponent)
        return result

    # Return the wrapper as the new function
    return wrapper

def Complex_fourier_series(func, T, N):
    c_n = 0
    array_c_n = []
    for k in range(N):
        intergrand = Fourier_series_exp_term(func, k , T)
        c_n = quad(lambda x: intergrand(x), 0, T)[0]#*1/(2*T)

        array_c_n.append(c_n)

    return array_c_n


def Create_pulse(func, T, offset=0):
    def wrapper(x):
        result = func(x-offset)*(np.heaviside(x-offset, 1)-np.heaviside(x-offset-T, 1))
        return result

    return wrapper


def Create_signal(func, T, r=100):
    def wrapper(x):
        result = 0
        for k in range(-r, r):
            result += func(x-k*T)
        return result

    return wrapper



class Vector_field():
    
    def __init__(self):
        self.x = np.linspace(-10, 10, 10)
        self.y = np.linspace(-10, 10, 10)        
        self.u, self.v = np.meshgrid(self.x, self.y)

    def __add__(self, value):
        self.u = self.u + value
        self.v = self.v + value
        return self

    def __iadd__(self, value):
        self.u = self.u + value
        self.v = self.v + value
        return self

#E = Vector_field()
#E += 10
#plt.quiver(E.x, E.y, E.u, E.v)
#plt.show()