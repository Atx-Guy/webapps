using System;
using System.Collections.Generic;
using System.Media;
using System.Windows;
using System.Windows.Input;  // For MouseEventArgs
using System.Windows.Threading;  // For DispatcherTimer
using System.Windows.Controls;   // For MenuItem and ContextMenu

namespace ClipboardManager
{
    public partial class MainWindow : Window
    {
        private List<string> clipboardHistory = new List<string>();
        private DispatcherTimer clipboardTimer;
        private bool historyCleared = false;  // Flag to check if history was cleared
        private string lastCopiedText = "";  // Store the last copied clipboard item

        public MainWindow()
        {
            InitializeComponent();
            StartClipboardWatcher();
        }

        // Start clipboard timer for checking clipboard content
        private void StartClipboardWatcher()
        {
            clipboardTimer = new DispatcherTimer();  // Initialize timer
            clipboardTimer.Interval = TimeSpan.FromMilliseconds(100);  // Check every 100 ms (faster polling)
            clipboardTimer.Tick += ClipboardTimer_Tick;  // Event handler
            clipboardTimer.Start();  // Start the timer
        }

        // This method will run every 100 ms and check the clipboard
        private void ClipboardTimer_Tick(object sender, EventArgs e)
        {
            try
            {
                string currentText = Clipboard.GetText();

                // Avoid adding the current clipboard content if it matches the last copied item
                if (!string.IsNullOrWhiteSpace(currentText) && !clipboardHistory.Contains(currentText) && !historyCleared)
                {
                    // If it's not the same as the last copied, add to history
                    if (currentText != lastCopiedText)
                    {
                        clipboardHistory.Add(currentText);
                        ClipboardListBox.Items.Add(currentText);
                    }

                    // Update the last copied text
                    lastCopiedText = currentText;
                }
            }
            catch (Exception ex)
            {
                // Handle any clipboard access issues gracefully
                Console.WriteLine("Error accessing clipboard: " + ex.Message);
            }
        }

        // Handle item click event to copy item to clipboard
        private void ClipboardList_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (ClipboardListBox.SelectedItem != null)
            {
                // Copy the selected item to clipboard
                Clipboard.SetText(ClipboardListBox.SelectedItem.ToString());
                SystemSounds.Beep.Play();  // Play sound on success
            }
        }

        // Clear clipboard history
        private void ClearList_Click(object sender, RoutedEventArgs e)
        {
            clipboardHistory.Clear();
            ClipboardListBox.Items.Clear();
            historyCleared = true;  // Set flag to ignore clipboard changes temporarily

            // Reset flag after a brief delay to resume clipboard monitoring
            DispatcherTimer resetFlagTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(500)  // Reset flag after 500 ms
            };
            resetFlagTimer.Tick += (s, args) =>
            {
                historyCleared = false;  // Reset the flag
                resetFlagTimer.Stop();  // Stop the timer
            };
            resetFlagTimer.Start();
        }

        // Edit selected clipboard entry
        private void EditMenuItem_Click(object sender, RoutedEventArgs e)
        {
            if (ClipboardListBox.SelectedItem != null)
            {
                string selectedItem = ClipboardListBox.SelectedItem.ToString();

                // Show the EditDialog to let the user modify the text
                EditDialog editDialog = new EditDialog(selectedItem);
                if (editDialog.ShowDialog() == true)
                {
                    string editedText = editDialog.EditedText;

                    if (!string.IsNullOrWhiteSpace(editedText) && editedText != selectedItem)
                    {
                        // Update history and list
                        clipboardHistory[clipboardHistory.IndexOf(selectedItem)] = editedText;
                        ClipboardListBox.Items[ClipboardListBox.Items.IndexOf(selectedItem)] = editedText;
                        SystemSounds.Beep.Play();  // Play sound on success
                    }
                }
            }
        }

        private void ClearAllButton_Click(object sender, RoutedEventArgs e)
        {
            // Clear the clipboard list
            ClipboardListBox.Items.Clear();

            // Optional: Play a sound or show a message that the list was cleared
            SystemSounds.Beep.Play();
        }

        // Delete selected clipboard entry
        private void DeleteMenuItem_Click(object sender, RoutedEventArgs e)
        {
            if (ClipboardListBox.SelectedItem != null)
            {
                string selectedItem = ClipboardListBox.SelectedItem.ToString();

                // Remove from history and list
                clipboardHistory.Remove(selectedItem);
                ClipboardListBox.Items.Remove(selectedItem);
                SystemSounds.Beep.Play();  // Play sound on success
            }
        }
    }
}
