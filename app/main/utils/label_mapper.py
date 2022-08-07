def label_mapper(label):
    if label == "mel":
        class_name = "melanoma"
    elif label == "df":
        class_name = "dermatofibroma"
    elif label == "nv":
        class_name = "melanocytic nevi"
    elif label == "akiec":
        class_name = "Actinic keratoses and intraepithelial carcinoma / Bowen's disease"
    elif label == "bcc":
        class_name = "basal cell carcinoma"
    elif label == "vasc":
        class_name = "vascular lesions"
    elif label == "bkl":
        class_name = "benign keratosis-like lesions (solar lentigines / seborrheic keratoses and lichen-planus like keratoses"
    else:
        class_name = "unknown mostly no infection"
    return class_name
