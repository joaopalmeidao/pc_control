# PC Control

PC Control is a web application that allows you to control the brightness and volume of your PC remotely using a web interface.

## Features

- Adjust screen brightness
- Adjust system volume
- Swagger UI for API documentation

## Technologies Used

- Frontend: React, TypeScript, Material-UI
- Backend: Flask, Python
- API Documentation: Swagger UI

## Installation

### Backend

1. Navigate to the backend directory:
    ```sh
    cd /E:/Programacao/pc_control/backend
    ```
2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the backend server:
    ```sh
    python server.py
    ```

### Frontend

1. Navigate to the frontend directory:
    ```sh
    cd /E:/Programacao/pc_control/frontend
    ```
2. Install the required packages:
    ```sh
    npm install
    ```
3. Run the frontend application:
    ```sh
    npm run dev
    ```

## Usage

1. Ensure both the backend server and frontend application are running.
2. Open your web browser and navigate to `http://localhost:3000`.
3. Use the sliders to adjust the brightness and volume of your PC.

## API Documentation

The API documentation is available at `http://localhost:5000/api/docs`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.