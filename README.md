# Results


https://github.com/user-attachments/assets/9e57b351-0c34-4688-939d-1cf14cd0adfc

[Dance Challenge - 1999 NCT Mark](https://www.youtube.com/shorts/jWmFXYKDzMs)

![image](https://github.com/user-attachments/assets/443c6bd4-2621-4ebf-bc6f-4e72ba2b347d)
Used [Rokoko](https://www.rokoko.com/) to export a `.BVH` file from a video I recorded 💃🏻

Also used [Animated Drawings](https://github.com/facebookresearch/AnimatedDrawings) to apply the dance to the character drawing.

# How to use

> [!Note]
> You must create the OpenAI API key and Azure Blob key before continuing!

- Clone this repository
```bash
git clone https://github.com/heewoneha/capstone-api.git && \
cd capstone-api
```

- Set the env variable

```.env
# `.env`
AZURE_STORAGE_CONTAINER_NAME="YOUR_VALUE"
AZURE_STORAGE_CONNECTION_STRING="YOUR_VALUE"
AZURE_PUBLIC_STORAGE_CONTAINER_NAME="YOUR_VALUE"
AZURE_PUBLIC_CONNECTION_STRING="YOUR_VALUE"
OPEN_AI_API_KEY="YOUR_VALUE"
```

- Run the server using Docker
```bash
docker compose build
docker compose up
```
