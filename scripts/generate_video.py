import os
import cv2


def run(path):

    image_folder = os.path.join(path, "ImagesRefined0")
    video_name = os.path.join(path, "ouptut.mp4")
    images = [img for img in os.listdir(image_folder) if img.endswith((".JPG", ".jpg", ".jpeg", ".png"))]
    images = sorted(images)
    print("Images:", images)

    # Set frame from the first image
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Video writer to create .avi file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 format
    video = cv2.VideoWriter(video_name, fourcc, 2, (width, height))

    # Appending images to video
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    # Release the video file
    video.release()
    cv2.destroyAllWindows()
    print("Video generated successfully!")

def main():
    output_path = "/home/emmahaidacher/Masterthesis/MasterThesis/tests/buddha2/mvsplat360/output/"
    for folder in os.listdir(output_path):
        test_folder = os.path.join(output_path, folder)
        run(test_folder)


if __name__ == "__main__":
    main()