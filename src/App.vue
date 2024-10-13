<template>
  <div class="div_chatCont">
    <div class="massange_cont">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="{ 'user-message': msg.isUser, 'api-message': !msg.isUser }"
      >
        <!-- Сообщение пользователя -->
        <div
          v-if="msg.isUser && msg.type === 'text'"
          class="user-message-content"
        >
          {{ msg.text }}
        </div>
        <div
          v-else-if="!msg.isUser && msg.type === 'text'"
          class="api-message-content"
        >
          <img
            src="../public/Frame.svg"
            alt=""
            class="api-message-content_img"
          />
          <div v-html="formatApiResponse(msg.text)"></div>
        </div>
        <!-- Сообщение с файлом -->
        <div
          v-if="msg.isUser && msg.type === 'file'"
          class="user-message-content file-message"
        >
          <div class="file-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="22"
              viewBox="0 0 18 22"
              fill="none"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M3.72414 10.0812C3.72414 9.64633 4.14098 9.29375 4.65517 9.29375H13.3448C13.859 9.29375 14.2759 9.64633 14.2759 10.0812C14.2759 10.5162 13.859 10.8687 13.3448 10.8687H4.65517C4.14098 10.8687 3.72414 10.5162 3.72414 10.0812ZM3.72414 13.2312C3.72414 12.7963 4.14098 12.4437 4.65517 12.4437H13.3448C13.859 12.4437 14.2759 12.7963 14.2759 13.2312C14.2759 13.6662 13.859 14.0187 13.3448 14.0187H4.65517C4.14098 14.0187 3.72414 13.6662 3.72414 13.2312ZM3.72414 16.3812C3.72414 15.9463 4.14098 15.5938 4.65517 15.5938H10.2414C10.7556 15.5938 11.1724 15.9463 11.1724 16.3812C11.1724 16.8162 10.7556 17.1687 10.2414 17.1687H4.65517C4.14098 17.1687 3.72414 16.8162 3.72414 16.3812Z"
                fill="white"
              />
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M2.17241 2.075C2.09011 2.075 2.01117 2.10266 1.95297 2.15188C1.89477 2.20111 1.86207 2.26788 1.86207 2.3375V19.6625C1.86207 19.7321 1.89477 19.7989 1.95297 19.8481C2.01117 19.8973 2.09011 19.925 2.17241 19.925H15.8276C15.9099 19.925 15.9888 19.8973 16.047 19.8481C16.1052 19.7989 16.1379 19.7321 16.1379 19.6625V6.5375H11.7931C11.5462 6.5375 11.3094 6.45453 11.1348 6.30685C10.9602 6.15916 10.8621 5.95886 10.8621 5.75V2.075H2.17241ZM12.7241 3.18866L14.8213 4.9625H12.7241V3.18866ZM0 2.3375C0 1.32267 0.972621 0.5 2.17241 0.5H11.7931C12.04 0.5 12.2768 0.58295 12.4515 0.730606L17.7274 5.19311C17.8138 5.26624 17.8824 5.35306 17.9292 5.44862C17.9759 5.54417 18 5.64658 18 5.75V19.6625C18 20.6773 17.0274 21.5 15.8276 21.5H2.17241C0.972621 21.5 0 20.6773 0 19.6625V2.3375Z"
                fill="white"
              />
            </svg>
          </div>
          <div class="file-name">
            <div class="file-name_cont">
              {{ msg.fileName }}
              <p class="file-type">Document</p>
            </div>
          </div>
        </div>
        <!-- Ответ API на сообщение с файлом -->
        <div
          v-else-if="!msg.isUser && msg.type === 'file'"
          class="api-message-content"
        >
          <img
            src="../public/Frame.svg"
            alt=""
            class="api-message-content_img"
          />
          Response from the API: {{ formatApiResponse(msg.apiResponse) }}
        </div>
      </div>
    </div>

    <div class="input-wrapper">
      <div class="input-container">
        <div class="attachment-icon" @click="triggerFileInput">
          <!-- SVG иконка для добавления файлов -->
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="14"
            height="20"
            viewBox="0 0 14 20"
            fill="none"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M4 5C4 2.23858 6.2386 0 9 0C11.7614 0 14 2.23858 14 5V13C14 16.866 10.866 20 7 20C3.13401 20 0 16.866 0 13V7C0 6.44772 0.44772 6 1 6C1.55228 6 2 6.44772 2 7V13C2 15.7614 4.23858 18 7 18C9.7614 18 12 15.7614 12 13V5C12 3.34315 10.6569 2 9 2C7.3431 2 6 3.34315 6 5V13C6 13.5523 6.4477 14 7 14C7.5523 14 8 13.5523 8 13V7C8 6.44772 8.4477 6 9 6C9.5523 6 10 6.44772 10 7V13C10 14.6569 8.6569 16 7 16C5.3431 16 4 14.6569 4 13V5Z"
              fill="white"
            />
          </svg>
        </div>
        <input v-model="message" type="text" placeholder="Write a request" />
        <input
          type="file"
          ref="fileInput"
          style="display: none"
          @change="handleFileUpload"
        />
        <div class="send-icon" @click="sendMessage">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="icon"
            width="20"
            height="18"
            viewBox="0 0 20 18"
            fill="none"
          >
            <path
              d="M2.35903 6.2606L3.02572 7.4496C3.45015 8.20659 3.66235 8.58501 3.66235 8.99999C3.66235 9.41496 3.45015 9.79338 3.02573 10.5504L2.35903 11.7394C0.460639 15.1251 -0.488558 16.8182 0.251636 17.6577C0.991831 18.4971 2.7446 17.7156 6.25014 16.1526L15.8711 12.2242C18.7454 11.017 20.1825 10.4134 20.1825 8.99999C20.1825 7.58662 18.7454 6.98302 15.8711 5.7758L6.25014 1.84739C2.7446 0.284417 0.991831 -0.497064 0.251636 0.342398C-0.488558 1.18186 0.460639 2.87492 2.35903 6.2606Z"
              fill="#4C4C4C"
            />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // Импортируем axios

export default {
  data() {
    return {
      message: "", // Переменная для хранения введенного сообщения
      messages: [], // Список сообщений
    };
  },
  methods: {
    sendMessage() {
      if (this.message.trim()) {
        // Добавляем текстовое сообщение пользователя
        this.messages.push({ text: this.message, isUser: true, type: "text" });
        this.message = ""; // Очищаем поле после отправки

        // Имитация ответа от API через 1 секунду
        setTimeout(() => {
          this.messages.push({
            text: "Response from the API",
            isUser: false,
            type: "text",
          });
        }, 1000);
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];

      if (file) {
        console.log("The file has been uploaded:", file);
        // Добавляем сообщение с файлом в чат
        this.messages.push({
          fileName: file.name,
          isUser: true,
          type: "file",
        });
        // Отправляем файл на API
        const way = "https://2254-2a12-5940-afb9-00-2.ngrok-free.app/upload";
        const formData = new FormData();
        formData.append("file", file);

        // Добавляем текст сообщения, если нужно
        formData.append("message", this.message);
        try {
          console.log("Sending file...");
          const response = await axios.post(way, formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });

          console.log("Response from the API:", response.data);
          // Извлекаем текст из результата
          const apiText =
            response.data.result && response.data.result.length > 0
              ? response.data.result[0]
              : "No response";

          // Добавляем сообщение с ответом от API
          this.messages.push({
            fileName: file.name,
            isUser: false,
            type: "file",
            apiResponse: apiText,
          });
        } catch (error) {
          console.error("Error sending the file:", error);
          this.messages.push({
            text: "Error sending the file",
            isUser: false,
            type: "text",
          });
        }
      }
    },
    formatApiResponse(responseText) {
      // Форматирование текста для лучшей читаемости
      return responseText.replace(/\n/g, "");
    },
  },
};
</script>

<style>
@font-face {
  font-family: "Atom";
  src: url("/src/fonts/Atom-Medium.otf") format("otf");
  src: url("/src/fonts/Atom-Light.otf") format("otf");
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: "Atom", sans-serif;
}

.file-name_cont {
  display: flex;
  flex-direction: column;
}
.file-type {
  margin: 0px;
  height: 14px;
  align-self: stretch;
  color: #4c4c4c;
  font-family: Atom;
  font-size: 14px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.massange_cont {
  height: 760px;
  width: 100%;
  padding: 10px;
  overflow-y: auto;
}

.user-message {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.user-message-content {
  display: inline-flex;
  height: 44px;
  padding: 0px 24px;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  border-radius: 60px 0px 60px 60px;
  background: #2f2f2f;
  color: #fff;
}

.api-message-content {
  display: flex;
  align-items: flex-start; /* Выравниваем контент по верху */
  width: 861px;
  min-height: 91px; /* Минимальная высота блока */
  max-height: auto; /* Позволяет блоку расти по высоте */
  flex-shrink: 0;
  color: #fff;
  font-size: 16px;
  font-weight: 500;
  line-height: normal;
  padding: 14px;
  margin-bottom: 10px;
  overflow-y: auto; /* Добавляем прокрутку по вертикали, если текст превышает высоту блока */
}

.file-message {
  display: flex;
  height: 56px;
  padding: 5px;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  border-radius: 10px;
  border: 1px solid #2f2f2f;
  background: #212121;
}

.file-icon {
  display: flex;
  width: 46px;
  height: 46px;

  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  border-radius: 5px;
  background: #00a6a6;
  margin-right: 10px;
}

.file-name {
  color: #fff;
  font-size: 16px;
}

/* Стилизация полосы прокрутки */
::-webkit-scrollbar {
  width: 5px;
  background: #151319;
}

/* Стилизация ползунка */
::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 50px;
}

body {
  padding-left: 260px;
  padding-right: 260px;
  background: #212121;
  display: flex;
  justify-content: center;
}

.input-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.input-container {
  display: flex;
  align-items: center;
  background-color: #333;
  border-radius: 30px;
  padding: 10px 15px;
  width: 100%;
  max-width: 600px;
}

.attachment-icon {
  margin-right: 10px;
  cursor: pointer;
}

input {
  flex: 1;
  background: none;
  border: none;
  color: #ccc;
  font-size: 16px;
  outline: none;
  padding: 10px;
}

input::placeholder {
  color: #666;
}

.send-icon {
  margin-left: 10px;
  cursor: pointer;
}

.send-icon svg {
  width: 20px;
  height: 18px;
  fill: #4c4c4c;
}
.api-message-content_img {
  margin-right: 10px;
  position: relative;
  bottom: 14px;
}
.icon path {
  transition: fill 0.3s ease;
}

.icon:hover path {
  fill: #ffffff;
}
</style>
