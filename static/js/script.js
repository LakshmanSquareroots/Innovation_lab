function handleImageUpload(event) {
    const fileInput = document.getElementById("image-upload");
    const uploadedImage = document.getElementById("uploaded-image");
    const uploadSymbol = document.getElementById("upload-symbol");
    const modelSelect = document.getElementById("model-selection");

    if (fileInput.files.length) {
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = "block";
            uploadSymbol.style.display = "none";
        };
        reader.readAsDataURL(file);
        modelSelect.disabled = false;
    } else {
        uploadedImage.style.display = "none";
        uploadSymbol.style.display = "flex";
        modelSelect.disabled = true;
    }
}

function processImage() {
    const fileInput = document.getElementById("image-upload");
    const modelSelect = document.getElementById("model-selection");
    const warningText = document.getElementById("warning-text");
    const loadingPopup = document.getElementById("loading-popup");

    if (!fileInput.files.length) {
        alert("Please upload an image first.");
        return;
    }

    if (modelSelect.value === "select-model") {
        warningText.textContent = "Please select a model.";
        return;
    } else {
        warningText.textContent = "";
    }

    loadingPopup.style.display = "flex";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Call the ModelClass endpoint with the selected model
    fetch(`/ModelClass/${modelSelect.value}/`, {
        method: "POST",
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        loadingPopup.style.display = "none";

        const processedImage = document.getElementById("processed-image");
        const processedSymbol = document.getElementById("processed-symbol");

        // Convert blob to object URL to display processed image
        const imageUrl = URL.createObjectURL(blob);
        processedImage.src = imageUrl;
        processedImage.style.display = "block";
        processedSymbol.style.display = "none";
    })
    .catch(error => {
        loadingPopup.style.display = "none";
        warningText.textContent = "Error processing the image. Please try again.";
        console.error("Error:", error);
    });
}

function clearProcessedImage() {
    const processedImage = document.getElementById("processed-image");
    const processedSymbol = document.getElementById("processed-symbol");
    processedImage.src = "";
    processedImage.style.display = "none";
    processedSymbol.style.display = "flex";
}
