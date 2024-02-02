import gradio as gr
import requests


def display_contents(uploaded_file: str) -> str:
    """Reads the uploaded .txt file and returns its contents."""
    if uploaded_file is None:
        return "No file uploaded"

    if not uploaded_file.endswith(".txt"):
        return "Enter a valid txt file"

    api_url = "http://api:8000/summarize/"

    with open(uploaded_file, "rb") as file:
        files = {"file": (uploaded_file, file)}

        response = requests.post(api_url, files=files)

    if response.status_code == 200:
        print("File sent successfully. Response:")

    else:
        print("Failed to send file. Status code:", response.status_code)

    summary = response.text
    return summary


demo = gr.Interface(
    fn=display_contents,
    inputs=gr.File(label="Upload a .txt file"),
    outputs="text",
    title="Text File Display App",
    description="Upload a .txt file and see its summary.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=3000)
