
window.addEventListener('beforeunload', moveFile);

function moveFile() {
    fetch('/api/move-file',
        {method: 'POST', headers: {'Content-Type': 'application/json'},})
        .then(response => {if (!response.ok) console.log('File moved successfully');})
        .catch(error => {console.error('Error:', error);});
}

document.addEventListener("DOMContentLoaded",
    function ()
    {
         const chatIcon = document.getElementById('chat-icon');
         const chatWidget = document.getElementById('chat-widget');
         const chatOutput = document.getElementById('chat-output');
         const userInput = document.getElementById('user-input');
         const minimizeBtn = document.getElementById('minimize-btn');
         const bookBtn = document.getElementById('book-btn');

         chatIcon.addEventListener('click', function ()
         {
             chatWidget.style.display = 'block';
             chatIcon.style.display = 'none';
         });

         minimizeBtn.addEventListener('click', function ()
         {
             chatWidget.style.display = 'none';
             chatIcon.style.display = 'block';
         });

         userInput.addEventListener('keypress', function (event)
         {
             if (event.key === 'Enter' && userInput.value.trim() !== '')
             {
                 sendMessage(userInput.value);
                 userInput.value = '';
             }
         });

         bookBtn.addEventListener('click', function ()
         {
             sendMessage('Book Free Consultation');
         });

         function sendMessage(message)
         {
            appendMessage(message, true); 
            fetch('/api/chat',
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {appendMessage(data.reply, false); })
                .catch(error => {console.error('Error : ', error); });
        }

        function appendMessage(message, isUser = false) {
            const messageContainer = document.createElement('div');
            messageContainer.classList.add('message-container');
            messageContainer.style.clear = 'both'; 
            messageContainer.style.display = 'flex';
            messageContainer.style.alignItems = 'center';
        
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            if (isUser) {
                messageElement.classList.add('user-message');
                messageContainer.style.marginTop = '25px';
                messageContainer.style.justifyContent = 'flex-end';
                messageElement.style.clear = 'both';
            } else {
                messageElement.classList.add('bot-message');
                messageContainer.style.marginTop = '25px';

                messageElement.style.clear = 'both';
            }
            messageElement.innerHTML = message;
        

            if (isUser) {
                messageContainer.appendChild(messageElement);
            } else {
                messageContainer.appendChild(messageElement);
            }

            // Apply animation class based on message type
            if (isUser) {
                messageElement.classList.add('user-message-animation');
            } else {
                messageElement.classList.add('bot-message-animation');
            }
        
            chatOutput.appendChild(messageContainer);
        
            // Auto-scroll to bottom
            chatOutput.scrollTop = chatOutput.scrollHeight;
        }
       
    });
