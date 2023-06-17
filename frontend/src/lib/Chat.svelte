<script context="module">
    import { writable } from 'svelte/store';
    import { initializeApp } from 'firebase/app';
    import { getDatabase, ref, set, onValue } from "firebase/database";
    import { v4 as uuidv4 } from 'uuid';

    // Function to delete a cookie by name
    function deleteCookie(cookieName) {
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;`;
    };

    function getCookie(cookieName) {
        const name = cookieName + "=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i];
                while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1);
                }
                if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
                }
            }

            return null;
    };

    let chat_id_val = getCookie('cowp_chat_id');
    let chat_id = (chat_id_val || uuidv4());
    document.cookie = `cowp_chat_id=${chat_id}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;

    export const messageTextStore = writable('');
    export const messagesStore = writable([]);
    let message_text = '';
    
    messageTextStore.subscribe(value => {
        message_text = value;
    });
    
    const firebaseConfig = {
        databaseURL: "https://cloud-whitepapers-index-default-rtdb.firebaseio.com",
    };
    
    const app = initializeApp(firebaseConfig);
    const database = getDatabase(app);
    let chatMessagesRef = ref(database, 'chats/' + chat_id + '/messages');
    
    onValue(chatMessagesRef, (snapshot) => {
        messagesStore.set(snapshot.val() || []);
    });
    
    export async function sendChatMessage() {
        let msg = { content: message_text };
        messageTextStore.set(''); 
    
        await fetch('/api/chats/' + chat_id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(msg)
        });
    };
    
    export async function deleteChatHistory() {
        await fetch('/api/chats/' + chat_id, {method: 'DELETE'});
        deleteCookie('cowp_chat_id');
        messagesStore.set([]); 
    };
</script>
    