
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
         const estimationBtn = document.getElementById('estimation-btn');
         const contactBtn = document.getElementById('contact-btn');

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

         estimationBtn.addEventListener('click', function ()
         {
             appendMessage('You : Calculate Price Estimation');
             calculate();
         });

         contactBtn.addEventListener('click', function ()
         {
             appendMessage('You : Need Contact Details');
             contactDetails();
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
        
        
        
        function contactDetails() {
            clearChatOutput();
            const contactmsg = document.createElement('div');
            contactmsg.innerHTML = "Magick : We’d Love to Hear From You<br>" +
                "<b>Our toll-free number :</b> 1800 270 3068<br>" +
                "<b>Mail your queries to :</b> talktous@magickhome.com<br><br>" +
                "<b>Visit our MagickHome Showroom : </b><br>" +
                "Door No – AA 127 to 133,<br>" +
                "4th Avenue, Main Road,<br>" +
                "Shanthi Colony, Anna Nagar,<br>" +
                "Chennai, Tamil Nadu 600040."
            chatOutput.appendChild(contactmsg);
        }
        
        function calculate() {
            clearChatOutput();
            const cal = document.createElement('div');
            cal.innerHTML = "Magick : For a detailed quote, Kindly click the below link. " +
                "Our design expert will contact you." +
                "<center><b><a href=https://www.magickhome.com/india/quick-quote target=\"_blank\">Quick-quote</a></b></center><br>"
            chatOutput.appendChild(cal);
        }
        
        function clearChatOutput() {
            // Get all children of chatOutput except the default content div
            const children = Array.from(chatOutput.children).filter(child => child.id !== "default-content");
            // Remove all children except the default content div
            children.forEach(child => child.remove());
        }
        
    });
