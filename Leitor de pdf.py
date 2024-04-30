import PyPDF2
import tkinter as tk
from tkinter import filedialog
import os

class PDFKeywordSplitter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Leitor de PDF")

        self.keyword = tk.StringVar()
        self.total_pages = tk.StringVar()
        self.pdf_pages = []
        self.selected_file = tk.StringVar()
        self.folder_counter = 1  # Inicializando o contador de pastas

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Palavra-chave:").grid(row=0, column=0, padx=5, pady=5)
        self.keyword_entry = tk.Entry(self, textvariable=self.keyword)
        self.keyword_entry.grid(row=0, column=1, padx=5, pady=5)

        self.select_button = tk.Button(self, text="Selecionar PDF", command=self.select_pdf)
        self.select_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.file_label = tk.Label(self, textvariable=self.selected_file, wraplength=300)
        self.file_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.clear_button = tk.Button(self, text="Limpar", command=self.clear_fields)
        self.clear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.split_button = tk.Button(self, text="Extrair PDF", command=self.split_pdf)
        self.split_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(self, text="Total de Páginas:").grid(row=5, column=0, padx=5, pady=5)
        tk.Label(self, textvariable=self.total_pages).grid(row=5, column=1, padx=5, pady=5)

        self.page_listbox = tk.Listbox(self)
        self.page_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if file_path:
            self.selected_file.set("Arquivo selecionado: " + file_path)
            self.clear_results()

    def clear_fields(self):
        self.keyword.set("")
        self.selected_file.set("")
        self.total_pages.set("")
        self.page_listbox.delete(0, tk.END)

    def split_pdf(self):
        keyword = self.keyword.get()
        if not keyword:
            tk.messagebox.showerror("Erro", "Por favor, insira uma palavra-chave.")
            return

        file_path = self.selected_file.get().replace("Arquivo selecionado: ", "")
        if not file_path:
            tk.messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF.")
            return

        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            output_folder = os.path.dirname(file_path) + f"/pages_{self.folder_counter}/"
            os.makedirs(output_folder, exist_ok=True)
            self.folder_counter += 1  # Incrementando o contador de pastas
            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text().lower()
                if keyword in page_text:
                    writer = PyPDF2.PdfWriter()
                    writer.add_page(page)
                    output_path = f"{output_folder}page_{page_num}.pdf"
                    with open(output_path, "wb") as output_file:
                        writer.write(output_file)
            tk.messagebox.showinfo("Sucesso", "PDF foi separado em páginas individuais!")

    def clear_results(self):
        self.keyword.set("")
        self.total_pages.set("")
        self.pdf_pages = []
        self.page_listbox.delete(0, tk.END)

if __name__ == "__main__":
    app = PDFKeywordSplitter()
    app.mainloop()

