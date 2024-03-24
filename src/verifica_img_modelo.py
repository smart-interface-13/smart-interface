import matplotlib.pyplot as plt
import os

NUM_EXAMPLES = 5
IMAGES_PATH = "gestos_data_sample"

# Get the list of labels from the list of folder names.
labels = [i for i in os.listdir(IMAGES_PATH) if os.path.isdir(os.path.join(IMAGES_PATH, i))]

# Create subplots outside the loop for labels
fig, axs = plt.subplots(len(labels), NUM_EXAMPLES, figsize=(15, 10))

# Show the images.
for idx, label in enumerate(labels):
    label_dir = os.path.join(IMAGES_PATH, label)
    example_filenames = os.listdir(label_dir)
    num_examples = min(NUM_EXAMPLES, len(example_filenames))
    for i in range(num_examples):
        img_path = os.path.join(label_dir, example_filenames[i])
        axs[idx, i].imshow(plt.imread(img_path))
        axs[idx, i].get_xaxis().set_visible(False)
        axs[idx, i].get_yaxis().set_visible(False)
    for j in range(num_examples, NUM_EXAMPLES):
        axs[idx, j].axis('off')  # Oculta ejes adicionales si no hay suficientes ejemplos
    fig.suptitle(f'Mostrando {NUM_EXAMPLES} ejemplos de cada categoria')

plt.tight_layout()
plt.show()