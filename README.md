## NEWTON'S BACKWARD DIFFERENCE CALCULATOR - Numerical Differentiation

A simple web-based tool for estimating the first and second derivatives of a function using Newton's Backward Difference Method. This method is part of numerical differentiation techniques used in cases where only tabulated data is available. It is used to approximate the derivatives of a function at the last point in a uniformly spaced dataset. It uses Python for the method and Streamlit for the user-interface.

---

---

## FORMULAS:

**First Derivative:**
\[
f'(x_n) \approx \frac{1}{h} \left( \nabla y_n + \frac{1}{2} \nabla^2 y_n + \frac{1}{3} \nabla^3 y_n + \frac{1}{4} \nabla^4 y_n \right)
\]

**Second Derivative:**
\[
f''(x_n) \approx \frac{1}{h^2} \left( \nabla^2 y_n + \nabla^3 y_n + \frac{11}{12} \nabla^4 y_n \right)
\]

Where:

- \( h \) is the uniform spacing between x-values.
- \( \nabla^k y_n \) are the backward difference terms.
- \( x_n \) is the last value of \( x \).

---

---

## HOW TO RUN

> Prerequisites

- Python 3.x installed
- Streamlit library

1. Install required dependencies:

   ```bash
   pip install streamlit numpy pandas matplotlib
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

3. A browser window will open automatically showing the interface.

---

---

## SAMPLE INPUTS and EXPECTED OUTPUTS

**Sample 1**
| x | f(x) |
| --- | ------ |
| 1.4 | 4.0552 |
| 1.6 | 4.9530 |
| 1.8 | 6.0496 |
| 2.0 | 7.3891 |
| 2.2 | 9.0250 |

**Evaluate at:**
x = 2.2

**Expected Output:**
f'(2.2) = 9.02142
f''(2.2) = 8.96292

**Sample 2**
| x | f(x) |
| --- | ------ |
| 0.0 | 2.0000 |
| 1.0 | 6.0000 |
| 2.0 | 12.0000 |
| 3.0 | 20.0000 |
| 4.0 | 30.0000 |
| 5.0 | 42.0000 |

**Evaluate at:**  
x = 4.0

**Expected Output:**
f'(4.0) = 11.0000
f''(4.0) = 2.0000

---

---

## FILES INCLUDED

- `README.md` — Project overview, setup instructions, usage examples, and documentation
- `app.py` — Main Streamlit application for computing backward difference and derivatives
- `design.css` — Custom CSS styling for inputs, buttons, and layout
- `background.png` — Background image used in the app

---

---

## FEATURES

- Interactive input fields for entering data points.
- Calculates first and second derivative using Newton's backward formula.
- Displays the difference table and full solution with math equations.
- Shows a graph of the input function and evaluation point.

---

---

## DEVELOPER

Developed by `Reisha Vien Aizl Gaan`, a Computer Engineering student from USTP CDO.  
Built in pursuit of knowledge, growth, and a passing grade in her Numerical Methods course.

---

---

## LICENSE

This project is intended for educational use and is free to use or modify.
Serves as the Final Term Performance Innovative Task for CPE223 - Numerical Methods.
