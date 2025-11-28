import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Recipe App", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None

def login(username, password):
    r = requests.post(f"{API_URL}/users/login",
                      json={"username": username, "password": password})
    if r.status_code == 200:
        data = r.json()
        st.session_state.api_key = data["api_key"]
        return True
    return False


def register(username, password):
    r = requests.post(f"{API_URL}/users/register",
                      json={"username": username, "password": password})
    return r.status_code == 200


def login_page():
    st.title(" Login to Recipe App")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        st.subheader("Sign in")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(user, pwd):
                st.success("Logged in!")
                st.session_state.logged_in = True
                st.session_state.username = user
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        st.subheader("Register")
        new_user = st.text_input("New username", key="reg_user")
        new_pwd = st.text_input("New password", type="password", key="reg_pwd")

        if st.button("Create Account"):
            if register(new_user, new_pwd):
                st.success("Account created! You can log in now.")
            else:
                st.error("Username already exists.")


def main_page():
    st.sidebar.title(f" Logged in as: {st.session_state.username}")

    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.api_key = None
        st.rerun()

    st.title("Recipe App with Nutritional Analysis")

    tab1, tab2, tab3 = st.tabs(["Add Recipe", "My Recipes", "Nutrition Analysis"])

    with tab1:
        st.subheader("Create a new recipe")

        recipe_title = st.text_input("Recipe name")
        recipe_description = st.text_area("Description")
        ingredients_raw = st.text_area(
            "Ingredients (name, amount, unit)",
            placeholder="egg, 50, g\nflour, 100, g"
        )

        if st.button("Save recipe"):
            ingredients_list = []
            for line in ingredients_raw.splitlines():
                try:
                    name, amount, unit = [x.strip() for x in line.split(",")]
                    ingredients_list.append({
                        "name": name,
                        "amount": float(amount),
                        "unit": unit,
                        "calories": 0
                    })
                except:
                    st.warning(f"Neispravan format: {line}")

            payload = {
                "title": recipe_title,
                "description": recipe_description,
                "ingredients": ingredients_list
            }

            r = requests.post(
                f"{API_URL}/recipes/",
                json=payload,
                headers={"X-API-Key": st.session_state.api_key}
            )

            if r.status_code == 200:
                st.success("Recipe saved!")
            else:
                st.error("Error saving recipe.")

    with tab2:
        st.subheader("My Recipes")

        r = requests.get(
            f"{API_URL}/recipes/mine",
            headers={"X-API-Key": st.session_state.api_key}
        )

        if r.status_code == 200:
            recipes = r.json()
            if not recipes:
                st.info("No recipes yet.")

            for recipe in recipes:
                st.write(f"### {recipe['title']}")
                st.write(recipe["description"])
                for ing in recipe["ingredients"]:
                    st.write(f"- {ing['name']}: {ing['amount']} {ing['unit']}")
                st.divider()

        else:
            st.error("Could not load recipes.")

    with tab3:
        st.subheader("Ingredient nutritional analysis")

        ingredients_input = st.text_area(
            "Enter ingredients",
            placeholder="egg, 50, g\nflour, 100, g"
        )

        if st.button("Analyze"):
            ingredients_list = []
            for line in ingredients_input.splitlines():
                try:
                    name, amount, unit = [x.strip() for x in line.split(",")]
                    ingredients_list.append({
                        "name": name,
                        "amount": float(amount),
                        "unit": unit
                    })
                except:
                    st.warning(f"Invalid line: {line}")

            r = requests.post(
                f"{API_URL}/nutrition/analyze",
                json={"ingredients": ingredients_list},
                headers={"X-API-Key": st.session_state.api_key}
            )

            if r.status_code == 200:
                data = r.json()
                st.write("### Total")
                st.json(data["totals"])
                st.write("### Breakdown")
                st.json(data["breakdown"])
            else:
                st.error("Analysis error.")


if st.session_state.logged_in:
    main_page()
else:
    login_page()

