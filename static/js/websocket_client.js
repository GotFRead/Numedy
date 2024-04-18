var client_id = Date.now();
var uls = document.getElementById("messages");
document.querySelector("#messageText").addEventListener("input", onInput);
let errors = document.getElementById("errors");
const messages_for_errors_code = new Map([
  [1, "Timeout ERROR check your input"],
  [2, "Found unsupported symbol"],
  [3, "Nothing NOT FOUND, check your input"],
]);

let timeout;

function onInput(event) {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    sendMessage(event);
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

  let info = string_.split('\n')

  console.log(info);

  if (!info) {
    console.warn("Not Match Values");
    return;
  }

  payload["device_and_port"] = info[1].split('Изменить: ')[1];
  payload["setting"] = info[3].split('Новые настройки: ')[1];

  console.log(payload);

  return payload;
}

async function on_accept_button_click(event) {
  const acceptDialog = document.querySelector("#accept");
  const vlanDialog = document.querySelector("#select_vlans");
  await fetch(`/vlan_preset_list/${client_id}`, {
    method: "POST",
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

async function get_vlan_preset_list() {
  let payload;
  let vlans = document.querySelector(".selector_container");

  try {
    let response = await fetch(`/vlan_preset_list/${client_id}`, {
      timeout: 1000,
    });
    payload = JSON.parse(await response.json());
  } catch (error) {
    console.log(error);
    return;
  }

  if (typeof payload === "undefined") return;

  for (const key in payload) {
    let selector_item = document.createElement("button");
    selector_item.className = "selector_item";
    selector_item.dataset["name"] = payload[key];
    selector_item.addEventListener("click", (e) => on_selector_item_click(e));
    selector_item.textContent = payload[key];
    vlans.appendChild(selector_item);
  }
}

function popup(event) {
  get_vlan_preset_list();
  const dialog = document.querySelector("#select_vlans");
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
  let switch_info = document.createElement("h4");
  switch_info.textContent = `Switch: ${item.switch} | Port: ${item.port}`;

  let description = document.createElement("p");
  description.textContent = `vlan: ${
    typeof item.vlan == "object" ? JSON.stringify(item.vlan) : item.vlan
  } | mac: ${item.mac} | description: ${item.description}`;
  message_container.appendChild(switch_info);
  message_container.appendChild(description);
  return message_container;
}

function Connect(address) {
  ws = new WebSocket(`ws://localhost:8000/session/${client_id}`);
  ws.onmessage = async function (event) {
    var messages = document.getElementById("messages");

    var message = document.createElement("li");
    var json_representation = JSON.parse(event.data);

    if (
      typeof json_representation == "object" &&
      "err" in json_representation &&
      messages_for_errors_code.has(json_representation["err"])
    ) {
      let message_container = document.createElement("p");
      let error_info = document.createElement("h4");
      error_info.textContent = messages_for_errors_code.get(
        json_representation["err"]
      );
      message_container.appendChild(error_info);
      errors.appendChild(message_container);
      return;
    }

    for (const key in json_representation) {
      messages.appendChild(createLiElem(json_representation[key]));
    }
    messages.appendChild(message);
  };
  ws.onerror = function (event) {
    window.preventDefault();
    console.log(event);
  };
  ws.onclose = function (event) {
    window.preventDefault();
    console.log(event);
  };
  ws.onopen = function (event) {
    console.log("start");
    flag = true;
  };
}

let start = Connect(1);

function sendMessage(event) {
  try {
    event.preventDefault();
    let input = document.getElementById("messageText");
    if (flag && input.value.length !== 0) {
      ws.send(input.value);
    }
  } catch (e) {
    console.log(e);
  }
}
