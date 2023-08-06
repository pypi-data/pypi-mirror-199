import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import re


def getAtomicMass(element_name):
    atomic_mass_dict = {
        # the masses of the elements
        'H': 1.008,
        'He': 4.003,
        'Li': 6.941,
        'Be': 9.012,
        'B': 10.81,
        'C': 12.01,
        'N': 14.01,
        'O': 16.00,
        'F': 19.00,
        'Ne': 20.18,
        'Na': 22.99,
        'Mg': 24.31,
        'Al': 26.98,
        'Si': 28.09,
        'P': 30.97,
        'S': 32.06,
        'Cl': 35.45,
        'K': 39.10,
        'Ar': 39.95,
        'Ca': 40.08,
        'Sc': 44.96,
        'Ti': 47.87,
        'V': 50.94,
        'Cr': 52.00,
        'Mn': 54.94,
        'Fe': 55.85,
        'Ni': 58.69,
        'Co': 58.93,
        'Cu': 63.55,
        'Zn': 65.38,
        'Ga': 69.72,
        'Ge': 72.63,
        'As': 74.92,
        'Se': 78.96,
        'Br': 79.90,
        'Kr': 83.80,
        'Rb': 85.47,
        'Sr': 87.62,
        'Y': 88.91,
        'Zr': 91.22,
        'Nb': 92.91,
        'Mo': 95.94,
        'Tc': 98.00,
        'Ru': 101.07,
        'Rh': 102.91,
        'Pd': 106.42,
        'Ag': 107.87,
        'Cd': 112.41,
        'In': 114.82,
        'Sn': 118.71,
        'Sb': 121.76,
        'I': 126.90,
        'Te': 127.60,
        'Xe': 131.29,
        'Cs': 132.91,
        'Ba': 137.33,
        'La': 138.91,
        'Ce': 140.12,
        'Pr': 140.91,
        'Nd': 144.24,
        'Pm': 145.00,
        'Sm': 150.36,
        'Eu': 151.96,
        'Gd': 157.25,
        'Tb': 158.93,
        'Dy': 162.50,
        'Ho': 164.93,
        'Er': 167.26,
        'Tm': 168.93,
        'Yb': 173.05,
        'Lu': 175.00,
        'Hf': 178.49,
        'Ta': 180.95,
        'W': 183.84,
        'Re': 186.21,
        'Os': 190.23,
        'Ir': 192.22,
        'Pt': 195.08,
        'Au': 196.97,
        'Hg': 200.59,
        'Tl': 204.38,
        'Pb': 207.2,
        'Bi': 208.98,
        'Th': 232.04,
        'Pa': 231.04,
        'U': 238.03,
        'Np': 237.05,
        'Pu': 244.06,
        'Am': 243.06,
        'Cm': 247.07,
        'Bk': 247.07,
        'Cf': 251.08,
        'Es': 252.08,
        'Fm': 257.10,
        'Md': 258.10,
        'No': 259.10,
        'Lr': 262.11,
        'Rf': 267.13,
        'Db': 270.13,
        'Sg': 271.14,
        'Bh': 270.13,
        'Hs': 277.15,
        'Mt': 276.15,
        'Ds': 281.17,
        'Rg': 280.17,
        'Cn': 285.18,
        'Nh': 284.18,
        'Fl': 289.19,
        'Mc': 288.19,
        'Lv': 293.20,
        'Ts': 294.21,
        'Og': 294.21
    }

    element_name = element_name.capitalize()

    if element_name in atomic_mass_dict:
        return atomic_mass_dict[element_name]
    else:
        return None


def toSymbol(element_name):
    symbol_dict = {
        'Hydrogen': 'H',
        'Helium': 'He',
        'Lithium': 'Li',
        'Beryllium': 'Be',
        'Boron': 'B',
        'Carbon': 'C',
        'Nitrogen': 'N',
        'Oxygen': 'O',
        'Fluorine': 'F',
        'Neon': 'Ne',
        'Sodium': 'Na',
        'Magnesium': 'Mg',
        'Aluminum': 'Al',
        'Silicon': 'Si',
        'Phosphorus': 'P',
        'Sulfur': 'S',
        'Chlorine': 'Cl',
        'Argon': 'Ar',
        'Potassium': 'K',
        'Calcium': 'Ca',
        'Scandium': 'Sc',
        'Titanium': 'Ti',
        'Vanadium': 'V',
        'Chromium': 'Cr',
        'Manganese': 'Mn',
        'Iron': 'Fe',
        'Cobalt': 'Co',
        'Nickel': 'Ni',
        'Copper': 'Cu',
        'Zinc': 'Zn',
        'Gallium': 'Ga',
        'Germanium': 'Ge',
        'Arsenic': 'As',
        'Selenium': 'Se',
        'Bromine': 'Br',
        'Krypton': 'Kr',
        'Rubidium': 'Rb',
        'Strontium': 'Sr',
        'Yttrium': 'Y',
        'Zirconium': 'Zr',
        'Niobium': 'Nb',
        'Molybdenum': 'Mo',
        'Technetium': 'Tc',
        'Ruthenium': 'Ru',
        'Rhodium': 'Rh',
        'Palladium': 'Pd',
        'Silver': 'Ag',
        'Cadmium': 'Cd',
        'Indium': 'In',
        'Tin': 'Sn',
        'Antimony': 'Sb',
        'Tellurium': 'Te',
        'Iodine': 'I',
        'Xenon': 'Xe',
        'Cesium': 'Cs',
        'Barium': 'Ba',
        'Lanthanum': 'La',
        'Cerium': 'Ce',
        'Praseodymium': 'Pr',
        'Neodymium': 'Nd',
        'Promethium': 'Pm',
        'Samarium': 'Sm',
        'Europium': 'Eu',
        'Gadolinium': 'Gd',
        'Terbium': 'Tb',
        'Dysprosium': 'Dy',
        'Holmium': 'Ho',
        'Erbium': 'Er',
        'Thulium': 'Tm',
        'Ytterbium': 'Yb',
        'Lutetium': 'Lu',
        'Hafnium': 'Hf',
        'Tantalum': 'Ta',
        'Tungsten': 'W',
        'Rhenium': 'Re',
        'Osmium': 'Os',
        'Iridium': 'Ir',
        'Platinum': 'Pt',
        'Gold': 'Au',
        'Mercury': 'Hg',
        'Thallium': 'Tl',
        'Lead': 'Pb',
        'Bismuth': 'Bi',
        'Polonium': 'Po',
        'Astatine': 'At',
        'Radon': 'Rn',
        'Francium': 'Fr',
        'Radium': 'Ra',
        'Actinium': 'Ac',
        'Thorium': 'Th',
        'Protactinium': 'Pa',
        'Uranium': 'U',
        'Neptunium': 'Np',
        'Plutonium': 'Pu',
        'Americium': 'Am',
        'Curium': 'Cm',
        'Berkelium': 'Bk',
        'Californium': 'Cf',
        'Einsteinium': 'Es',
        'Fermium': 'Fm',
        'Mendelevium': 'Md',
        'Nobelium': 'No',
        'Lawrencium': 'Lr',
        'Rutherfordium': 'Rf',
        'Dubnium': 'Db',
        'Seaborgium': 'Sg',
        'Bohrium': 'Bh',
        'Hassium': 'Hs',
        'Meitnerium': 'Mt',
        'Darmstadtium': 'Ds',
        'Roentgenium': 'Rg',
        'Copernicium': 'Cn',
        'Nihonium': 'Nh',
        'Flerovium': 'Fl',
        'Moscovium': 'Mc',
        'Livermorium': 'Lv',
        'Tennessine': 'Ts',
        'Oganesson': 'Og'
    }
    return symbol_dict.get(element_name, "Element not found")


def toName(symbol):
    symbol_dict = {
        'H': 'Hydrogen',
        'He': 'Helium',
        'Li': 'Lithium',
        'Be': 'Beryllium',
        'B': 'Boron',
        'C': 'Carbon',
        'N': 'Nitrogen',
        'O': 'Oxygen',
        'F': 'Fluorine',
        'Ne': 'Neon',
        'Na': 'Sodium',
        'Mg': 'Magnesium',
        'Al': 'Aluminum',
        'Si': 'Silicon',
        'P': 'Phosphorus',
        'S': 'Sulfur',
        'Cl': 'Chlorine',
        'Ar': 'Argon',
        'K': 'Potassium',
        'Ca': 'Calcium',
        'Sc': 'Scandium',
        'Ti': 'Titanium',
        'V': 'Vanadium',
        'Cr': 'Chromium',
        'Mn': 'Manganese',
        'Fe': 'Iron',
        'Co': 'Cobalt',
        'Ni': 'Nickel',
        'Cu': 'Copper',
        'Zn': 'Zinc',
        'Ga': 'Gallium',
        'Ge': 'Germanium',
        'As': 'Arsenic',
        'Se': 'Selenium',
        'Br': 'Bromine',
        'Kr': 'Krypton',
        'Rb': 'Rubidium',
        'Sr': 'Strontium',
        'Y': 'Yttrium',
        'Zr': 'Zirconium',
        'Nb': 'Niobium',
        'Mo': 'Molybdenum',
        'Tc': 'Technetium',
        'Ru': 'Ruthenium',
        'Rh': 'Rhodium',
        'Pd': 'Palladium',
        'Ag': 'Silver',
        'Cd': 'Cadmium',
        'In': 'Indium',
        'Sn': 'Tin',
        'Sb': 'Antimony',
        'Te': 'Tellurium',
        'I': 'Iodine',
        'Xe': 'Xenon',
        'Cs': 'Cesium',
        'Ba': 'Barium',
        'La': 'Lanthanum',
        'Ce': 'Cerium',
        'Pr': 'Praseodymium',
        'Nd': 'Neodymium',
        'Pm': 'Promethium',
        'Sm': 'Samarium',
        'Eu': 'Europium',
        'Gd': 'Gadolinium',
        'Tb': 'Terbium',
        'Dy': 'Dysprosium',
        'Ho': 'Holmium',
        'Er': 'Erbium',
        'Tm': 'Thulium',
        'Yb': 'Ytterbium',
        'Lu': 'Lutetium',
        'Hf': 'Hafnium',
        'Ta': 'Tantalum',
        'W': 'Tungsten',
        'Re': 'Rhenium',
        'Os': 'Osmium',
        'Ir': 'Iridium',
        'Pt': 'Platinum',
        'Au': 'Gold',
        'Hg': 'Mercury',
        'Tl': 'Thallium',
        'Pb': 'Lead',
        'Bi': 'Bismuth',
        'Po': 'Polonium',
        'At': 'Astatine',
        'Rn': 'Radon',
        'Fr': 'Francium',
        'Ra': 'Radium',
        'Ac': 'Actinium',
        'Th': 'Thorium',
        'Pa': 'Protactinium',
        'U': 'Uranium',
        'Np': 'Neptunium',
        'Pu': 'Plutonium',
        'Am': 'Americium',
        'Cm': 'Curium',
        'Bk': 'Berkelium',
        'Cf': 'Californium',
        'Es': 'Einsteinium',
        'Fm': 'Fermium',
        'Md': 'Mendelevium',
        'No': 'Nobelium',
        'Lr': 'Lawrencium',
        'Rf': 'Rutherfordium',
        'Db': 'Dubnium',
        'Sg': 'Seaborgium',
        'Bh': 'Bohrium',
        'Hs': 'Hassium',
        'Mt': 'Meitnerium',
        'Ds': 'Darmstadtium',
        'Rg': 'Roentgenium',
        'Cn': 'Copernicium',
        'Nh': 'Nihonium',
        'Fl': 'Flerovium',
        'Mc': 'Moscovium',
        'Lv': 'Livermorium',
        'Ts': 'Tennessine',
        'Og': 'Oganesson'
    }
    return symbol_dict.get(symbol, "Element not found")


def plotElementAtom(atomic_number, symbol):
    # Get the number of protons and electrons
    num_protons = atomic_number
    num_electrons = atomic_number

    # Set up the positions of the protons and electrons
    proton_positions = [(0, 0)]
    electron_positions = []

    for i in range(num_electrons):
        angle = i * 2 * math.pi / num_electrons
        x = 0.8 * math.cos(angle)
        y = 0.8 * math.sin(angle)
        electron_positions.append((x, y))

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    # Plot the protons as red circles
    for pos in proton_positions:
        circle = patches.Circle(pos, 0.25, linewidth=2, fill=True, facecolor='red', edgecolor='red')
        ax.add_artist(circle)

    # Plot the electrons as green circles
    for pos in electron_positions:
        circle = patches.Circle(pos, 0.01, linewidth=2, fill=True, facecolor='yellow', edgecolor='orange')
        ax.add_artist(circle)

        # Add lines connecting the electrons to the nucleus
        line = patches.ConnectionPatch(pos, proton_positions[0], coordsA="data", coordsB="data", linewidth=1, alpha=0.5,
                                       edgecolor='gray')
        ax.add_artist(line)

    # Set the limits of the plot
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    # Add labels for the protons and electrons

    ax.text(0, 0.5, symbol, fontsize=24, ha='center', va='center')
    ax.text(0, -0.5, f"{num_protons} protons", fontsize=14, ha='center', va='center')
    ax.text(0.8, 0, f"{num_electrons} electrons", fontsize=14, ha='center', va='center')

    # Turn off the axis labels and ticks
    ax.axis('off')

    # Show the plot
    plt.show()


def concentrationTimeGraph(concentration_data, time_data):
    """
    Plots a concentration vs time graph given two lists of data: concentration_data and time_data
    """
    plt.plot(time_data, concentration_data)
    plt.xlabel('Time')
    plt.ylabel('Concentration')
    plt.title('Concentration vs Time')
    plt.show()


def plotLightWavelength(light_type):
    """
    Plots the wavelength of a type of light given its name as a string
    """
    wavelengths = {'gamma_ray': (0.01, 0.001), 'x-ray': (0.001, 10), 'ultraviolet': (10, 400), 'visible': (400, 700),
                   'infrared': (700, 1000000), 'microwave': (1000000, 100000000), 'radio': (100000000, 100000000000)}

    wavelength_range = wavelengths.get(light_type.lower(), None)
    if not wavelength_range:
        print(f"{light_type} is not a valid type of light.")
        return

    wave_length = np.linspace(wavelength_range[0], wavelength_range[1], 1000)
    wave_amplitude = np.sin(2 * np.pi * wave_length / (wavelength_range[1] - wavelength_range[0]))
    plt.plot(wave_length, wave_amplitude)
    plt.axhline(y=0, color='black', linestyle='--')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Amplitude')
    plt.title(f'{light_type.capitalize()} Light Wave')
    plt.show()


def write_net_ionic_equation(equation):
    """
    Takes in a chemical equation as a string and returns the net ionic equation as another string
    """
    # Split the equation into its reactants and products
    reactants, products = equation.split('->')

    # Split the reactants and products into individual compounds
    reactants = [compound.strip() for compound in reactants.split('+')]
    products = [compound.strip() for compound in products.split('+')]

    # Identify the ions present in each compound
    reactant_ions = [ion.strip() for compound in reactants for ion in compound.split(' ')]
    product_ions = [ion.strip() for compound in products for ion in compound.split(' ')]

    # Identify the spectator ions (ions that appear on both sides of the equation)
    spectator_ions = set(reactant_ions).intersection(product_ions)

    # Remove the spectator ions from the reactants and products
    net_reactants = [compound for compound in reactants if not any(ion in compound for ion in spectator_ions)]
    net_products = [compound for compound in products if not any(ion in compound for ion in spectator_ions)]

    # Combine the net reactants and products into the net ionic equation
    net_ionic_equation = ' + '.join(net_reactants) + ' -> ' + ' + '.join(net_products)

    return net_ionic_equation


ATOMS = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
         'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
         'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I',
         'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',
         'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au',
         'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U',
         'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db',
         'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']


def getAtoms():
    return ATOMS


def parseFormula(formula):
    # Regular expression pattern to match elements and their counts
    pattern = r'([A-Z][a-z]*)(\d*)'

    # Initialize dictionary to store number of atoms for each element
    atoms = {}

    # Iterate over each element in the formula
    for match in re.findall(pattern, formula):
        element, count = match
        if count == '':
            count = 1
        else:
            count = int(count)

        # Check if element is a valid symbol
        if element not in ATOMS:
            raise ValueError(f"element {element} is not valid")

        # Add the number of atoms for the element to the dictionary
        if element in atoms:
            atoms[element] += count
        else:
            atoms[element] = count

    return atoms


class Chemical:
    def __init__(self, name, formula, molar_mass):
        self.name = name
        self.formula = formula
        self.molar_mass = molar_mass

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_formula(self):
        return self.formula

    def set_formula(self, formula):
        self.formula = formula

    def get_molar_mass(self):
        return self.molar_mass

    def set_molar_mass(self, molar_mass):
        self.molar_mass = molar_mass

    def __str__(self):
        return f"{self.name} ({self.formula}), {self.molar_mass} g/mol"

    def calculate_mass(self, moles):
        return moles * self.molar_mass

    def calculate_moles(self, mass):
        return mass / self.molar_mass

    @staticmethod
    def calculate_density(mass, volume):
        return mass / volume

    @staticmethod
    def calculate_molarity(moles, volume):
        return moles / (volume / 1000)  # Volume is in mL, so convert to L

    @staticmethod
    def calculate_mass_percent(mass_component, mass_total):
        return (mass_component / mass_total) * 100

    @staticmethod
    def calculate_volume(moles, temperature, pressure):
        R = 0.0821  # Ideal gas constant (L⋅atm/K⋅mol)
        return (moles * R * temperature) / pressure

    def calculate_heat(self, mass, delta_T):
        return mass * self.get_specific_heat() * delta_T

    @staticmethod
    def get_specific_heat():
        # Returns the specific heat capacity of the chemical in J/g·K
        # This value is assumed to be constant over the temperature range of interest
        # Here, we're using a placeholder value of 4.18 J/g·K for water
        return 4.18

    def calculate_pH(self, concentration):
        # Calculates the pH of a solution of the chemical given its concentration
        # This function assumes that the chemical is a weak acid with a known pKa value
        # Here, we're using a placeholder pKa value of 4.75 for acetic acid
        pKa = 4.75
        return pKa + math.log10(concentration / self.calculate_conjugate_base_concentration(concentration))

    def calculate_conjugate_base_concentration(self, concentration):
        # Calculates the concentration of the conjugate base of the chemical in a solution of given concentration
        # This function assumes that the chemical is a weak acid with a known pKa value
        # Here, we're using a placeholder pKa value of 4.75 for acetic acid
        pKa = 4.75
        return 10 ** (pKa - self.calculate_pH(concentration))


def factorial(n):
    """
    Returns the factorial of n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def quadratic_formula(a, b, c):
    """
    Returns the roots of the quadratic equation ax^2 + bx + c = 0.
    """
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None
    elif discriminant == 0:
        return -b / (2 * a)
    else:
        root1 = (-b + discriminant ** 0.5) / (2 * a)
        root2 = (-b - discriminant ** 0.5) / (2 * a)
        return root1, root2


def solve_linear_equation(a, b):
    """
    Returns the solution to the linear equation ax + b = 0.
    """
    if a == 0 and b != 0:
        return None
    elif a == 0 and b == 0:
        return "Infinite solutions"
    else:
        return -b / a


def sin(__x):
    return math.sin(__x)


def cos(__x):
    return math.cos(__x)


def tan(__x):
    return math.tan(__x)


def asin(__x):
    return math.asin(__x)


def acos(__x):
    return math.acos(__x)


def atan(__x):
    return math.atan(__x)


def atan2(__x, __y):
    return math.atan2(__x, __y)
