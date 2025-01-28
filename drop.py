import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crop Image")

        # Variables de la clase
        self.img = None
        self.img_tk = None
        self.start_x = self.start_y = 0
        self.rect = None
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        # Botón para cargar la imagen
        self.btn_load = tk.Button(root, text="Cargar Imagen", command=self.load_image)
        self.btn_load.pack(pady=10)
         

        # Agregar los eventos de click y movimiento del mouse
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpeg;*.JPG")])
        if file_path:
            # Cargar la imagen seleccionada
            self.img = Image.open(file_path)
            self.img_tk = ImageTk.PhotoImage(self.img)
            
            # Configurar el tamaño del canvas
            self.canvas.config(width=self.img.width, height=self.img.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

    def on_button_press(self, event):
        """Detectar cuando el usuario presiona el botón izquierdo del ratón para comenzar a dibujar el rectángulo de selección."""
        if self.img is not None:
            self.start_x = event.x
            self.start_y = event.y
            # Crear un rectángulo vacío para mostrar la selección
            if self.rect:
                self.canvas.delete(self.rect)
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        """Actualizar el rectángulo mientras el usuario mueve el mouse."""
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        """Recortar la imagen cuando el usuario suelta el botón del ratón."""
        if self.rect:
            # Obtener las coordenadas del rectángulo de selección
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            if x1 != x2 and y1 != y2:  # Asegurarse de que se haya seleccionado una región válida
                self.crop_image(x1, y1, x2, y2)

    def crop_image(self, x1, y1, x2, y2):
        """Recortar la imagen y mostrarla en el canvas."""
        cropped_img = self.img.crop((x1, y1, x2, y2))
        self.img_tk = ImageTk.PhotoImage(cropped_img)
        
        # Limpiar el canvas y mostrar la imagen recortada
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
       

    

# Crear la ventana principal
root = tk.Tk()
app = ImageCropperApp(root)
root.mainloop()
