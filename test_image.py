from modules.image_generator import generate_image


prompt = """
Educational digital illustration of a large distributed
computing system, multiple computers connected together,
simple clean educational style, colorful, clear,
college textbook illustration, no text, no labels
"""


output = generate_image(
    prompt,
    "output/test_image.png"
)


print("Image generated successfully:")
print(output)