# CGPA Calculator

A Streamlit app that computes your SGPA and updated CGPA.

Defaults: CGPA 8.87, 117 credits completed, and five 3-credit courses (AI, ML, ASM, MPC, DOP).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Sign-in

The app requires Google sign-in and only lets in the emails listed in `allowed_emails`.
See [secrets.toml.example](secrets.toml.example): create a Google OAuth client (Web application),
add the `/oauth2callback` redirect URI, then put the values in `.streamlit/secrets.toml` locally
or in the Streamlit Cloud Secrets box. Without these secrets the app refuses to load.

## Deploy

Push to GitHub, then create an app on [Streamlit Community Cloud](https://share.streamlit.io) pointing at `app.py`.
