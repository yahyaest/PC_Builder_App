//export let components_list = new Array();
let components_list = new Array();
let data_name = $("#name-list").data();
data_name = data_name.name.split("'");
data_name = data_name.join('"');
data_name = JSON.parse(data_name);
let name_list = Object.values(data_name);
//console.log(name_list);

let data_type = $("#type-list").data();
data_type = data_type.name.split("'");
data_type = data_type.join('"');
data_type = JSON.parse(data_type);
let type_list = Object.values(data_type);
//console.log(type_list);

let data_price = $("#price-list").data();
data_price = data_price.name;
let price_list = data_price;
//console.log(price_list);

let data_rate = $("#rate-list").data();
data_rate = data_rate.name;
let rate_list = data_rate;
//console.log(rate_list);

let cpu_list = [];
let gpu_list = [];
let mother_board_list = [];
let pc_case_list = [];
let ram_list = [];
let hdd_list = [];
let ssd_list = [];
let power_supply_list = [];

for (let i = 1; i < data_name.length; i++) {
  if (i < 11) {
    cpu_list.push(data_name[i]);
  } else if (i < 16) {
    gpu_list.push(data_name[i]);
  } else if (i < 30) {
    mother_board_list.push(data_name[i]);
  } else if (i < 40) {
    pc_case_list.push(data_name[i]);
  } else if (i < 43) {
    ram_list.push(data_name[i]);
  } else if (i < 48) {
    hdd_list.push(data_name[i]);
  } else if (i < 52) {
    ssd_list.push(data_name[i]);
  } else {
    power_supply_list.push(data_name[i]);
  }
}

console.log(
  cpu_list,
  gpu_list,
  mother_board_list,
  pc_case_list,
  ram_list,
  hdd_list,
  ssd_list,
  power_supply_list
);

async function getData(id, option_class, list) {
  await sleep(1000);

  for (let index of list) {
    let option = document.createElement("div");
    option.setAttribute("class", `${option_class}`);
    let input = document.createElement("input");
    input.setAttribute("type", "radio");
    input.setAttribute("class", "radio");
    input.setAttribute("id", `${index}`);
    input.setAttribute("name", "category");

    let component_name = document.createElement("label");
    component_name.setAttribute("for", `${index}`);
    component_name.innerText = index;

    option.appendChild(input);
    option.appendChild(component_name);
    document.getElementById(`${id}`).append(option);
  }
}

async function search(
  id,
  option_class,
  list,
  select,
  option_contain,
  search_box
) {
  await sleep(1000);
  await getData(id, option_class, list);

  const selected = document.querySelector(`${select}`);
  const optionsContainer = document.querySelector(`${option_contain}`);
  const searchBox = document.querySelector(`${search_box}`);

  const optionsList = document.querySelectorAll(`.${option_class}`);

  selected.addEventListener("click", () => {
    optionsContainer.classList.toggle("active");

    searchBox.value = "";
    filterList("");

    if (optionsContainer.classList.contains("active")) {
      searchBox.focus();
    }
  });

  optionsList.forEach((o) => {
    o.addEventListener("click", () => {
      selected.innerHTML = o.querySelector("label").innerHTML;
      optionsContainer.classList.remove("active");
    });
  });

  searchBox.addEventListener("keyup", function (e) {
    filterList(e.target.value);
  });

  const filterList = (searchTerm) => {
    searchTerm = searchTerm.toLowerCase();
    optionsList.forEach((option) => {
      let label =
        option.firstElementChild.nextElementSibling.innerText.toLowerCase();
      if (label.indexOf(searchTerm) != -1) {
        option.style.display = "block";
      } else {
        option.style.display = "none";
      }
    });
  };
}

search(
  "cpu",
  "option",
  cpu_list,
  ".selected",
  ".options-container",
  ".search-box input"
);

search(
  "gpu",
  "option-2",
  gpu_list,
  ".selected-2",
  ".options-container-2",
  ".search-box-2 input"
);

search(
  "motherboard",
  "option-3",
  mother_board_list,
  ".selected-3",
  ".options-container-3",
  ".search-box-3 input"
);

search(
  "pc-case",
  "option-4",
  pc_case_list,
  ".selected-4",
  ".options-container-4",
  ".search-box-4 input"
);

search(
  "power-supply",
  "option-5",
  power_supply_list,
  ".selected-5",
  ".options-container-5",
  ".search-box-5 input"
);

search(
  "ram",
  "option-6",
  ram_list,
  ".selected-6",
  ".options-container-6",
  ".search-box-6 input"
);

search(
  "ssd",
  "option-7",
  ssd_list,
  ".selected-7",
  ".options-container-7",
  ".search-box-7 input"
);

search(
  "hdd",
  "option-8",
  hdd_list,
  ".selected-8",
  ".options-container-8",
  ".search-box-8 input"
);

function get_components() {
  components_list.push(document.querySelector(".selected").innerText);
  for (let i = 2; i < 9; i++) {
    let index = ".selected-" + i;
    let component = document.querySelector(`${index}`).innerText;
    components_list.push(component);
    if (component.startsWith("Choose")) {
      alert(
        "One or many fields are not selected. Plese verify before setting an order"
      );
      return;
    }
  }
  console.log(components_list);
  localStorage.setItem("transfer", components_list);
  window.document.location = appDomain + "/order";
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

//document.querySelector("selected").innerText;
//document.querySelector('.selected').innerText;
