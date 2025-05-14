import streamlit as st
import numpy as np
import pandas as pd
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(page_title="Newton's Backward Difference Calculator", layout="centered")

def backward_difference_table(y_values):
    n = len(y_values)
    table = [y_values.copy()]
    for i in range(1, n):
        col = [table[i-1][j+1] - table[i-1][j] for j in range(n - i)]
        table.append(col)
    return table

def first_derivative(diffs, h):
    return (1/h) * (diffs[1][-1] + (1/2)*diffs[2][-1] + (1/3)*diffs[3][-1] + (1/4)*diffs[4][-1])

def second_derivative(diffs, h):
    return (1/(h**2)) * (diffs[2][-1] + diffs[3][-1] + (11/12)*diffs[4][-1])

def main():
    img_base64 = get_base64_image("background.png")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🧮 Newton's Backward Difference Calculator")

    num_points = st.number_input("Number of data points", min_value=5, value=5, step=1)

    st.subheader("Enter x and f(x) values:")
    x_values, y_values = [], []

    subscript_digits = "₀₁₂₃₄₅₆₇₈₉"

    for i in range(num_points):
        sub_i = ''.join(subscript_digits[int(d)] for d in str(i))
        cols = st.columns(2)
        with cols[0]:
            x = st.number_input(f"x{sub_i}", key=f"x_{i}", format="%.2f")
        with cols[1]:
            y = st.number_input(f"f(x{sub_i})", key=f"y_{i}", format="%.4f")
        x_values.append(x)
        y_values.append(y)

    target_x = st.number_input("At what x do you want to evaluate f′(x) and f″(x)?", key="target_x", format="%.2f")

    if st.button("Calculate"):
        if target_x not in x_values:
            st.error("The value must be the last xₙ (i.e., the highest x).")
            return

        h = x_values[1] - x_values[0]
        xn_index = x_values.index(target_x)

        if xn_index < 4:
            st.error("Need at least 5 values ending at the selected xₙ.")
            return

        trimmed_y = y_values[xn_index - 4: xn_index + 1]
        trimmed_x = x_values[xn_index - 4: xn_index + 1]
        diffs = backward_difference_table(trimmed_y)

        # Build difference table for display
        max_len = len(diffs[0])
        padded_diffs = []
        for i in range(len(diffs)):
            padded = [''] * (max_len - len(diffs[i])) + diffs[i]
            padded_diffs.append(padded)

        df_table = pd.DataFrame(list(zip(*padded_diffs)), columns=["y", "∇y", "∇²y", "∇³y", "∇⁴y"])
        df_table.insert(0, "x", trimmed_x)

        f_prime = first_derivative(diffs, h)
        f_double_prime = second_derivative(diffs, h)

        st.subheader("📘 Difference Table:")
        st.dataframe(df_table.style.format(precision=4), use_container_width=True)

        st.subheader("🧠 Step-by-step Solution:")
        st.latex(r"f'(x_n) = \frac{1}{h} \left( \nabla y_n + \frac{1}{2} \nabla^2 y_n + \frac{1}{3} \nabla^3 y_n + \frac{1}{4} \nabla^4 y_n \right)")
        st.latex(fr"f'(x_n) = \frac{{1}}{{{h:.4f}}} \left( {diffs[1][-1]:.4f} + \frac{{1}}{{2}} \cdot {diffs[2][-1]:.4f} + \frac{{1}}{{3}} \cdot {diffs[3][-1]:.4f} + \frac{{1}}{{4}} \cdot {diffs[4][-1]:.4f} \right)")
        st.latex(fr"f'(x_n) = {f_prime:.5f}")

        st.latex(r"f''(x_n) = \frac{1}{h^2} \left( \nabla^2 y_n + \nabla^3 y_n + \frac{11}{12} \nabla^4 y_n \right)")
        st.latex(fr"f''(x_n) = \frac{{1}}{{{h**2:.4f}}} \left( {diffs[2][-1]:.4f} + {diffs[3][-1]:.4f} + \frac{{11}}{{12}} \cdot {diffs[4][-1]:.4f} \right)")
        st.latex(fr"f''(x_n) = {f_double_prime:.5f}")

        st.subheader("✅ Final Result:")
        st.latex(fr"f'({target_x:.4f}) \approx \boxed{{{f_prime:.5f}}}")
        st.latex(fr"f''({target_x:.4f}) \approx \boxed{{{f_double_prime:.5f}}}")

if __name__ == "__main__":
    main()
