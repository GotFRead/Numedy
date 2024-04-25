var client_id = Date.now();
var uls = document.getElementById("messages");
document.querySelector("#messageText").addEventListener("input", onInput);
let errors = document.getElementById("errors");
const messages_for_errors_code = new Map([
  ["ERROR", "Timeout ERROR check your input"],
  ["SUCCESS", "Your product was found!"],
]);

let timeout;

function onInput(event) {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    get_product_by_name(event);
    uls.textContent = "";
    errors.textContent = "";
  }, 450);
}

let flag = false;

function get_message(event) {
  if (event.target.classList.contains("message")) {
    return event.target;
  } else {
    return event.target.parentElement;
  }
}

function on_cancel_button_click(event) {
  const acceptDialog = document.querySelector("#accept");
  acceptDialog.close();
}

function get_dialog_payload(string_) {
  let payload = {};

  let info = string_.split("\n");

  console.log(info);

  if (!info) {
    console.warn("Not Match Values");
    return;
  }

  payload["device_and_port"] = info[1].split("Изменить: ")[1];
  payload["setting"] = info[3].split("Новые настройки: ")[1];

  console.log(payload);

  return payload;
}

async function on_accept_button_click(event) {
  // TODO Переделать под запросы удаление
  const acceptDialog = document.querySelector("#accept");
  const vlanDialog = document.querySelector("#select_vlans");
  await fetch(`/product/${client_id}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(get_dialog_payload(acceptDialog.textContent)),
    timeout: 1000,
  });
  acceptDialog.close();
  vlanDialog.close();
}

function on_selector_item_click(event) {
  const acceptDialog = document.querySelector("#accept");
  const selectVlanDialog = document.querySelector("#select_vlans");
  const target = event.target;
  acceptDialog.querySelector("#device").textContent =
    selectVlanDialog.querySelector("#title").textContent;
  acceptDialog.querySelector("#before").textContent =
    selectVlanDialog.querySelector("#old_info").textContent;
  acceptDialog.querySelector(
    "#after"
  ).textContent = `Новые настройки: ${target.dataset["name"]}`;
  acceptDialog.setAttribute("open", "true");
}

function popup(event) {
  const dialog = document.querySelector("#accept");
  let title = dialog.querySelector("#title");
  let event_content = get_message(event);
  let message_title = event_content.querySelector("h4").textContent;
  let message_payload = event_content
    .querySelector("p")
    .textContent.split(" | ")[0];

  title.textContent = `Изменить: ${message_title}`;
  let old_info = dialog.querySelector("#old_info");
  old_info.innerHTML = `Текущие настройки: ${message_payload}`;
  dialog.setAttribute("open", "true");
}

function createLiElem(item) {
  let message_container = document.createElement("div");
  message_container.className = "message";
  message_container.onclick = popup;
  let product_info = document.createElement("h4");
  product_info.textContent = `Id: ${item.id} | Name: ${item.name}`;

  let description = document.createElement("p");
  description.textContent = `storage: ${item.storage} | weight: ${item.weight}`;
  message_container.appendChild(product_info);
  message_container.appendChild(description);
  return message_container;
}

async function get_product_by_name(event) {
  let request = document.getElementById("messageText");
  let response = await fetch(`/products/search_product/${request.value}`, {
    timeout: 1000,
  });

  await result_product_representation(await response.json());
}

async function get_all(event) {
  let response = await fetch(`/products/${client_id}`, {
    timeout: 1000,
  });
  payload = JSON.parse(await response.json());

  await result_product_representation(payload);
}

async function result_product_representation(payload) {
  try {
    var messages = document.getElementById("messages");
    var json_representation = payload;

    if (
      typeof json_representation == "object" &&
      messages_for_errors_code.has(json_representation.status)
    ) {
      let message_container = document.createElement("p");
      let error_info = document.createElement("h4");
      error_info.textContent = messages_for_errors_code.get(
        json_representation.status
      );
      message_container.appendChild(error_info);
      errors.appendChild(message_container);

      for (const key in json_representation.founded_objects) {
        messages.appendChild(createLiElem(json_representation.founded_objects[key]));
      }
      
      return;
    }
  } catch (error) {
    console.log(error);
    return;
  }
}
