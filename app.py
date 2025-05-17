import streamlit as st
import numpy as np
import pandas as pd
import base64
import matplotlib.pyplot as plt


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def load_local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(page_title="Newton's Backward Difference Calculator", layout="centered")


# Build backward difference table from y-values
def backward_difference_table(y_values):
    n = len(y_values)
    table = [y_values.copy()]
    for i in range(1, n):
        col = [table[i - 1][j + 1] - table[i - 1][j] for j in range(n - i)]
        table.append(col)
    return table


# First derivative approximation formula using backward differences
def first_derivative(diffs, h):
    return (1 / h) * (diffs[1][-1] + (1 / 2) * diffs[2][-1] + (1 / 3) * diffs[3][-1] + (1 / 4) * diffs[4][-1])


# Second derivative approximation formula using backward differences
def second_derivative(diffs, h):
    return (1 / (h ** 2)) * (diffs[2][-1] + diffs[3][-1] + (11 / 12) * diffs[4][-1])


def inject_bg_image(base64_image):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center top;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    # Load background and CSS if available
    try:
        img_base64 = get_base64_image("background.png")
        inject_bg_image(img_base64)
    except FileNotFoundError:
        pass

    try:
        load_local_css("design.css")
    except FileNotFoundError:
        pass

    st.markdown(
        """
        <div class="custom-title">
            <h1>Newton's Backward Difference</h1>
            <h3>Numerical Differentiation Calculator</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h4 style="font-size: 1.2em; margin-bottom: -2.5em;">Number of data points (min 5)</h4>', unsafe_allow_html=True
    )
    num_points = st.number_input("", min_value=5, value=5, step=1, key="num_points")

    st.markdown('<h4 style="font-size:1.2em; margin-bottom: -1.5em;">Enter x and f(x) values:</h4>', unsafe_allow_html=True)

    x_values, y_values = [], []
    subscript_digits = "₀₁₂₃₄₅₆₇₈₉"

    for i in range(num_points):
        sub_i = ''.join(subscript_digits[int(d)] for d in str(i))
        cols = st.columns(2)
        with cols[0]:
            x = st.number_input(f"x{sub_i}", key=f"x_{i}", format="%.4f")
        with cols[1]:
            y = st.number_input(f"f(x{sub_i})", key=f"y_{i}", format="%.4f")
        x_values.append(x)
        y_values.append(y)

    st.markdown(
        '<h4 style="font-size: 1.2em; margin-bottom: -2.5em;">At which x do you want to evaluate f′(x) and f″(x)?</h4>',
        unsafe_allow_html=True,
    )
    target_x = st.number_input("", key="target_x", format="%.4f")

    if st.button("Calculate"):
        if target_x not in x_values:
            st.error("The value must be one of the x-values you provided.")
            return

        xn_index = x_values.index(target_x)

        
        if xn_index < 4:
            st.error(
                "Need at least 5 consecutive data points ending at the selected x. "
                "Try selecting a later x-value or providing more data points."
            )
            return

        
        trimmed_x = x_values[xn_index - 4 : xn_index + 1]
        trimmed_y = y_values[xn_index - 4 : xn_index + 1]

        
        h = trimmed_x[1] - trimmed_x[0]
        if not all(np.isclose(trimmed_x[i + 1] - trimmed_x[i], h) for i in range(4)):
            st.error("x-values must be equally spaced for backward difference method.")
            return

        diffs = backward_difference_table(trimmed_y)


        max_len = len(diffs[0])
        padded_diffs = []
        for i in range(len(diffs)):
            padded = [''] * (max_len - len(diffs[i])) + diffs[i]
            padded_diffs.append(padded)

        df_table = pd.DataFrame(list(zip(*padded_diffs)), columns=["y", "∇y", "∇²y", "∇³y", "∇⁴y"])
        df_table.insert(0, "x", trimmed_x)

        f_prime = first_derivative(diffs, h)
        f_double_prime = second_derivative(diffs, h)

        st.subheader("Backward Difference Table")
        st.dataframe(df_table.style.format(precision=4), use_container_width=True)

        st.subheader("Step-by-step Solution")

        st.latex(
            r"f'(x_n) = \frac{1}{h} \left( \nabla y_n + \frac{1}{2} \nabla^2 y_n + \frac{1}{3} \nabla^3 y_n + \frac{1}{4} \nabla^4 y_n \right)"
        )
        st.latex(
            fr"f'(x_n) = \frac{{1}}{{{h:.4f}}} \left( {diffs[1][-1]:.6f} + \frac{{1}}{{2}} \cdot {diffs[2][-1]:.6f} + \frac{{1}}{{3}} \cdot {diffs[3][-1]:.6f} + \frac{{1}}{{4}} \cdot {diffs[4][-1]:.6f} \right)"
        )
        st.latex(fr"f'(x_n) = {f_prime:.6f}")

        st.latex(r"f''(x_n) = \frac{1}{h^2} \left( \nabla^2 y_n + \nabla^3 y_n + \frac{11}{12} \nabla^4 y_n \right)")
        st.latex(
            fr"f''(x_n) = \frac{{1}}{{{h ** 2:.6f}}} \left( {diffs[2][-1]:.6f} + {diffs[3][-1]:.6f} + \frac{{11}}{{12}} \cdot {diffs[4][-1]:.6f} \right)"
        )
        st.latex(fr"f''(x_n) = {f_double_prime:.6f}")

        st.subheader("Final Results")
        st.latex(fr"f'({target_x:.4f}) \approx \boxed{{{f_prime:.4f}}}")
        st.latex(fr"f''({target_x:.4f}) \approx \boxed{{{f_double_prime:.4f}}}")

        fig, ax = plt.subplots()

        ax.plot(x_values, y_values, 'o-', color='mediumvioletred', label='f(x)')
        ax.plot(target_x, y_values[xn_index], 'ro', label=f'f({target_x})')

        ax.annotate(
            f"({target_x:.4f}, {y_values[xn_index]:.4f})",
            (target_x, y_values[xn_index]),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center',
            color='white',
        )

        ax.set_facecolor("#660033")
        fig.patch.set_facecolor("#25001c")
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.set_title("Function Plot", color='white')
        ax.set_xlabel("x", color='white')
        ax.set_ylabel("f(x)", color='white')
        ax.legend(facecolor="#2a003f", edgecolor='white', labelcolor='white')

        st.pyplot(fig)


if __name__ == "__main__":
    main()
