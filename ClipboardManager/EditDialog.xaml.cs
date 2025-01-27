using System;
using System.Windows;

namespace ClipboardManager
{
    public partial class EditDialog : Window
    {
        public string EditedText { get; private set; }

        public EditDialog(string textToEdit)
        {
            InitializeComponent();

            // Set the TextBox text
            EditTextBox.Text = textToEdit;

            // Adjust the window width dynamically based on text length
            int length = textToEdit.Length;
            Width = Math.Max(300, length * 7); // Calculate width (minimum 300px)
        }

        private void SaveButton_Click(object sender, RoutedEventArgs e)
        {
            EditedText = EditTextBox.Text;
            DialogResult = true;
            Close();
        }
    }
}
