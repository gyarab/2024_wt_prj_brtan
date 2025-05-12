document.addEventListener("DOMContentLoaded", function () {
    let form = document.querySelector("form");
    if (form) {
        let fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.name = "multi_upload_obrazky";
        fileInput.multiple = true;
        fileInput.accept = "image/*";

        let label = document.createElement("label");
        label.innerText = "Nahrát více obrázků:";
        label.style.display = "block";
        label.style.marginTop = "20px";

        form.appendChild(label);
        form.appendChild(fileInput);
    }
});
