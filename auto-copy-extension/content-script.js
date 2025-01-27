// Content Script for Auto Copy Extension

let lastCopiedText = ''; // Store the last copied text
let lastCopyTime = 0; // Track the last copy time
const COPY_DELAY = 10000; // 10-second delay in milliseconds
let pasteButton = null; // Reference to the paste button

// Handle text selection events
document.addEventListener('mouseup', handleSelection);
document.addEventListener('keyup', handleSelection); // Add keyboard support

// Handle input field clicks
document.addEventListener('click', handleInputClick);

function handleSelection(event) {
  // Check if enough time has passed since the last copy
  const currentTime = Date.now();
  if (currentTime - lastCopyTime < COPY_DELAY) {
    console.log('Copy skipped: Too soon after last copy');
    return; // Exit if the delay hasn't passed
  }

  // Get the active element (where selection is happening)
  const activeElement = document.activeElement;

  // Check if the selection is in an input or textarea
  const isInput = activeElement?.tagName.match(/INPUT|TEXTAREA/i);
  const isContentEditable = activeElement?.isContentEditable;

  // Get the selected text
  let selection;
  if (isInput || isContentEditable) {
    // Handle input/textarea selections
    selection = activeElement.value.substring(
      activeElement.selectionStart,
      activeElement.selectionEnd
    ).trim();
  } else {
    // Handle regular text selections
    selection = window.getSelection().toString().trim();
  }

  // Only proceed if there's actual text selected
  if (selection) {
    // Copy to clipboard and show feedback
    navigator.clipboard.writeText(selection)
      .then(() => {
        lastCopiedText = selection; // Update the last copied text
        lastCopyTime = Date.now(); // Update the last copy time
        showCopiedFeedback(selection);
        console.log('Text copied to clipboard:', selection);
      })
      .catch(err => {
        showCopiedFeedback('Failed to copy!');
        console.error('Failed to copy text:', err);
      });
  }
}

function handleInputClick(event) {
  const target = event.target;

  // Check if the clicked element is an input or textarea
  if (target.tagName.match(/INPUT|TEXTAREA/i) || target.isContentEditable) {
    // If the paste button already exists, just update its position
    if (pasteButton) {
      pasteButton.style.left = `${event.clientX - 10}px`; // Position to the left of the cursor
      pasteButton.style.top = `${event.clientY + 10}px`; // Position below the cursor
      return;
    }

    // Create the paste button
    pasteButton = document.createElement('button');
    pasteButton.style.position = 'absolute';
    pasteButton.style.left = `${event.clientX - 10}px`; // Position to the left of the cursor
    pasteButton.style.top = `${event.clientY + 10}px`; // Position below the cursor
    pasteButton.style.zIndex = '2147483647'; // Maximum z-index
    pasteButton.style.background = 'transparent'; // Fully transparent background
    pasteButton.style.border = 'none'; // No border
    pasteButton.style.padding = '0'; // No padding
    pasteButton.style.cursor = 'pointer';
    pasteButton.style.opacity = '1'; // Fully visible (icon)
    pasteButton.style.transition = 'opacity 60s ease-in'; // Slow fade-in effect

    // Add the icon to the button
    const icon = document.createElement('img');
    icon.src = chrome.runtime.getURL('icons/paste.png'); // Load the icon from /icons/
    icon.style.width = '24px'; // Set icon size
    icon.style.height = '24px';
    icon.style.display = 'block';
    pasteButton.appendChild(icon);

    // Add hover effect
    pasteButton.addEventListener('mouseenter', () => {
      pasteButton.style.opacity = '0.8'; // Slightly transparent on hover
    });
    pasteButton.addEventListener('mouseleave', () => {
      pasteButton.style.opacity = '1'; // Fully visible when not hovered
    });

    // Add click event to paste the text
    pasteButton.addEventListener('click', () => {
      if (lastCopiedText) {
        if (target.isContentEditable) {
          // Handle contenteditable elements
          const range = document.createRange();
          range.selectNodeContents(target);
          range.collapse(false);
          const selection = window.getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
          document.execCommand('insertText', false, lastCopiedText);
        } else {
          // Handle input/textarea elements
          target.value = lastCopiedText;
          target.dispatchEvent(new Event('input', { bubbles: true })); // Trigger input event
        }
      }
      // Remove the button after being clicked, regardless of success
      pasteButton.remove();
      pasteButton = null; // Clear the reference
    });

    // Add the button to the document
    document.body.appendChild(pasteButton);

    // Remove the button if the user clicks outside the input field and button
    document.addEventListener('click', removePasteButtonOnOutsideClick);
  }
}

function removePasteButtonOnOutsideClick(event) {
  const target = event.target;

  // Check if the click is outside the paste button and input fields
  if (
    pasteButton &&
    !pasteButton.contains(target) &&
    !target.tagName.match(/INPUT|TEXTAREA/i) &&
    !target.isContentEditable
  ) {
    pasteButton.remove();
    pasteButton = null; // Clear the reference
    document.removeEventListener('click', removePasteButtonOnOutsideClick); // Clean up the listener
  }
}

// Visual feedback function
function showCopiedFeedback(text) {
  // Remove any existing feedback elements first
  const existingFeedback = document.querySelector('.auto-copy-feedback');
  if (existingFeedback) existingFeedback.remove();

  // Create the feedback element
  const feedback = document.createElement('div');
  
  // Add accessibility features
  feedback.setAttribute('role', 'status');
  feedback.setAttribute('aria-live', 'polite');
  
  // Style configuration
  feedback.textContent = `Copied: ${truncateText(text, 25)}`;
  feedback.className = 'auto-copy-feedback';
  Object.assign(feedback.style, {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    background: '#4CAF50',
    color: 'white',
    padding: '12px 20px',
    borderRadius: '4px',
    zIndex: '2147483647', // Maximum possible z-index
    fontSize: '14px',
    boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
    animation: 'slideIn 0.3s ease-out'
  });

  // Add to document
  document.documentElement.appendChild(feedback);
  
  // Auto-remove after timeout
  setTimeout(() => {
    feedback.style.animation = 'fadeOut 0.3s ease-in';
    setTimeout(() => feedback.remove(), 300);
  }, 1700);

  // Handle text truncation
  function truncateText(str, maxLength) {
    if (str.length <= maxLength) return str;
    return str.substring(0, maxLength) + '…';
  }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
`;
document.head.appendChild(style);