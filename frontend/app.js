const API_URL = "http://127.0.0.1:8000";

const SESSION_STORAGE_KEY = "minigpt_session_id";

let sessionId = getOrCreateSessionId();
let isLoading = false;


/* =========================================
   DOM ELEMENTS
   ========================================= */

const messages = document.getElementById("messages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");
const typingContainer = document.getElementById("typingContainer");
const apiStatus = document.getElementById("apiStatus");
const welcome = document.getElementById("welcome");
const historyList = document.getElementById("historyList");


/* =========================================
   SESSION
   ========================================= */

function createSessionId() {
    return `web-${crypto.randomUUID()}`;
}


function getOrCreateSessionId() {

    const existingSession =
        localStorage.getItem(
            SESSION_STORAGE_KEY
        );

    if (existingSession) {
        return existingSession;
    }

    const newSession =
        createSessionId();

    localStorage.setItem(
        SESSION_STORAGE_KEY,
        newSession
    );

    return newSession;
}


/* =========================================
   API STATUS
   ========================================= */

async function checkApiStatus() {

    try {

        const response = await fetch(
            `${API_URL}/health`
        );

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        apiStatus.textContent = "Connected";

    } catch (error) {

        apiStatus.textContent = "Offline";

    }
}


/* =========================================
   LOAD CHAT HISTORY
   ========================================= */

async function loadChatHistory() {

    try {

        const response = await fetch(
            `${API_URL}/sessions`
        );

        if (!response.ok) {
            throw new Error(
                "Unable to load chat history."
            );
        }

        const sessions =
            await response.json();

        renderChatHistory(sessions);

    } catch (error) {

        console.warn(
            "Could not load chat history:",
            error
        );

        historyList.innerHTML = "";

        const empty =
            document.createElement("div");

        empty.className =
            "history-empty";

        empty.textContent =
            "Unable to load conversations.";

        historyList.appendChild(empty);
    }
}


/* =========================================
   RENDER CHAT HISTORY
   ========================================= */

function renderChatHistory(sessions) {

    historyList.innerHTML = "";

    if (!sessions.length) {

        const empty =
            document.createElement("div");

        empty.className =
            "history-empty";

        empty.textContent =
            "No conversations yet.";

        historyList.appendChild(empty);

        return;
    }


    sessions.forEach(session => {

        const item =
            document.createElement("button");

        item.className =
            "history-item";


        if (
            session.session_id === sessionId
        ) {

            item.classList.add("active");

        }


        const icon =
            document.createElement("div");

        icon.className =
            "history-icon";

        icon.textContent =
            "◈";


        const text =
            document.createElement("div");

        text.className =
            "history-text";


        const title =
            document.createElement("span");

        title.className =
            "history-title";

        title.textContent =
            createChatTitle(
                session.first_message
            );


        const time =
            document.createElement("span");

        time.className =
            "history-time";

        time.textContent =
            formatTime(
                session.last_message_at
            );


        text.appendChild(title);

        text.appendChild(time);


        item.appendChild(icon);

        item.appendChild(text);


        item.addEventListener(
            "click",
            () => {
                openSession(
                    session.session_id
                );
            }
        );


        historyList.appendChild(item);

    });
}


/* =========================================
   CHAT TITLE
   ========================================= */

function createChatTitle(message) {

    if (!message) {
        return "New conversation";
    }

    const cleaned =
        message
            .replace(/\s+/g, " ")
            .trim();

    if (cleaned.length <= 38) {
        return cleaned;
    }

    return (
        cleaned.substring(0, 38) +
        "..."
    );
}


/* =========================================
   FORMAT TIME
   ========================================= */

function formatTime(timestamp) {

    if (!timestamp) {
        return "";
    }

    const date =
        new Date(
            timestamp.replace(" ", "T") + "Z"
        );

    if (Number.isNaN(date.getTime())) {
        return "";
    }

    const now = new Date();

    const difference =
        now.getTime() -
        date.getTime();

    const minutes =
        Math.floor(
            difference / 60000
        );


    if (minutes < 1) {
        return "Just now";
    }

    if (minutes < 60) {
        return `${minutes}m ago`;
    }


    const hours =
        Math.floor(
            minutes / 60
        );

    if (hours < 24) {
        return `${hours}h ago`;
    }


    const days =
        Math.floor(
            hours / 24
        );

    if (days < 7) {
        return `${days}d ago`;
    }


    return date.toLocaleDateString(
        undefined,
        {
            day: "numeric",
            month: "short"
        }
    );
}


/* =========================================
   OPEN SESSION
   ========================================= */

async function openSession(
    selectedSessionId
) {

    if (isLoading) {
        return;
    }

    sessionId =
        selectedSessionId;

    localStorage.setItem(
        SESSION_STORAGE_KEY,
        sessionId
    );


    messages.innerHTML = "";

    messages.appendChild(
        welcome
    );

    welcome.style.display =
        "none";


    try {

        const response = await fetch(
            `${API_URL}/sessions/${encodeURIComponent(sessionId)}/messages`
        );

        if (!response.ok) {
            throw new Error(
                "Unable to load conversation."
            );
        }

        const history =
            await response.json();


        if (!history.length) {

            welcome.style.display =
                "block";

            return;
        }


        history.forEach(message => {

            addMessage(
                message.role,
                message.content
            );

        });


        highlightActiveSession();

        scrollToBottom();

    } catch (error) {

        addMessage(
            "assistant",
            "Unable to load this conversation.",
            true
        );

    }
}


/* =========================================
   HIGHLIGHT ACTIVE SESSION
   ========================================= */

function highlightActiveSession() {

    const items =
        historyList.querySelectorAll(
            ".history-item"
        );

    items.forEach(item => {

        item.classList.remove(
            "active"
        );

    });

    /*
     * The history list will be refreshed
     * after each message, which keeps the
     * active session synchronized.
     */
}


/* =========================================
   LOAD CURRENT CONVERSATION
   ========================================= */

async function loadConversation() {

    try {

        const response = await fetch(
            `${API_URL}/sessions/${encodeURIComponent(sessionId)}/messages`
        );

        if (!response.ok) {
            throw new Error(
                "Unable to load conversation."
            );
        }

        const history =
            await response.json();


        if (!history.length) {
            return;
        }


        hideWelcome();


        history.forEach(message => {

            addMessage(
                message.role,
                message.content
            );

        });

    } catch (error) {

        console.warn(
            "Could not restore conversation:",
            error
        );

    }
}


/* =========================================
   SEND MESSAGE
   ========================================= */

async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (!message || isLoading) {
        return;
    }


    isLoading = true;

    sendBtn.disabled = true;


    hideWelcome();


    addMessage(
        "user",
        message
    );


    messageInput.value = "";

    resizeTextarea();


    showTyping();


    try {

        const response =
            await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        session_id:
                            sessionId,

                        message:
                            message
                    })
                }
            );


        if (!response.ok) {

            let errorMessage =
                "Something went wrong while contacting MiniGPT.";


            try {

                const errorData =
                    await response.json();


                if (errorData.detail) {

                    errorMessage =
                        Array.isArray(
                            errorData.detail
                        )
                            ? "Please enter a valid message."
                            : errorData.detail;

                }

            } catch {
                // Keep default error message.
            }


            throw new Error(
                errorMessage
            );
        }


        const data =
            await response.json();


        hideTyping();


        addMessage(
            "assistant",
            data.answer
        );


        addSources(
            data.sources
        );


        await loadChatHistory();

    } catch (error) {

        hideTyping();


        addMessage(
            "assistant",
            error.message ||
            "Unable to connect to MiniGPT.",
            true
        );

    } finally {

        isLoading = false;

        sendBtn.disabled = false;

        messageInput.focus();

    }
}


/* =========================================
   ADD MESSAGE
   ========================================= */

function addMessage(
    role,
    content,
    isError = false
) {

    const message =
        document.createElement("div");

    message.className =
        `message ${role}`;


    const avatar =
        document.createElement("div");

    avatar.className =
        "message-avatar";


    avatar.textContent =
        role === "assistant"
            ? "✦"
            : "●";


    const messageContent =
        document.createElement("div");

    messageContent.className =
        "message-content";


    if (isError) {

        messageContent.classList.add(
            "error-message"
        );

    }


    messageContent.textContent =
        content;


    message.appendChild(
        avatar
    );

    message.appendChild(
        messageContent
    );


    messages.appendChild(
        message
    );


    scrollToBottom();
}


/* =========================================
   ADD SOURCES
   ========================================= */

function addSources(sources) {

    if (
        !sources ||
        sources.length === 0
    ) {
        return;
    }


    const container =
        document.createElement("div");

    container.className =
        "sources";


    const title =
        document.createElement("div");

    title.className =
        "sources-title";

    title.textContent =
        "RETRIEVED SOURCES";


    container.appendChild(
        title
    );


    sources.forEach(source => {

        const card =
            document.createElement("div");

        card.className =
            "source-card";


        const meta =
            document.createElement("div");

        meta.className =
            "source-meta";


        let location =
            source.source ||
            "Unknown source";


        if (
            source.page !== undefined &&
            source.page !== null
        ) {

            location +=
                ` · Page ${source.page}`;

        }


        if (
            source.chunk !== undefined &&
            source.chunk !== null
        ) {

            location +=
                ` · Chunk ${source.chunk}`;

        }


        meta.textContent =
            `◈ ${location}`;


        const evidence =
            document.createElement("div");

        evidence.className =
            "source-evidence";


        evidence.textContent =
            source.evidence ||
            "No evidence preview available.";


        card.appendChild(
            meta
        );

        card.appendChild(
            evidence
        );


        container.appendChild(
            card
        );

    });


    messages.appendChild(
        container
    );


    scrollToBottom();
}


/* =========================================
   WELCOME
   ========================================= */

function hideWelcome() {

    if (welcome) {
        welcome.style.display =
            "none";
    }

}


/* =========================================
   TYPING
   ========================================= */

function showTyping() {

    typingContainer.style.display =
        "flex";

    scrollToBottom();

}


function hideTyping() {

    typingContainer.style.display =
        "none";

}


/* =========================================
   NEW CHAT
   ========================================= */

function newChat() {

    sessionId =
        createSessionId();


    localStorage.setItem(
        SESSION_STORAGE_KEY,
        sessionId
    );


    messages.innerHTML = "";


    messages.appendChild(
        welcome
    );


    welcome.style.display =
        "block";


    messageInput.value = "";

    resizeTextarea();

    highlightActiveSession();

    messageInput.focus();

}


/* =========================================
   TEXTAREA
   ========================================= */

function resizeTextarea() {

    messageInput.style.height =
        "auto";


    messageInput.style.height =
        `${Math.min(
            messageInput.scrollHeight,
            130
        )}px`;

}


/* =========================================
   SCROLL
   ========================================= */

function scrollToBottom() {

    requestAnimationFrame(() => {

        messages.scrollTo({
            top:
                messages.scrollHeight,

            behavior:
                "smooth"
        });

    });
}


/* =========================================
   EVENT LISTENERS
   ========================================= */

sendBtn.addEventListener(
    "click",
    sendMessage
);


newChatBtn.addEventListener(
    "click",
    newChat
);


messageInput.addEventListener(
    "input",
    resizeTextarea
);


messageInput.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


document
    .querySelectorAll(".suggestion")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                messageInput.value =
                    button.dataset.question;

                resizeTextarea();

                sendMessage();

            }
        );

    });


/* =========================================
   STARTUP
   ========================================= */

checkApiStatus();

loadChatHistory();

loadConversation();

messageInput.focus();
