let data_price = $("#price-list").data();
data_price = data_price.name;
let price_list = data_price;
console.log(price_list);

let data_name = $("#name-list").data();
data_name = data_name.name.split("'");
data_name = data_name.join('"');
data_name = JSON.parse(data_name);
let name_list = Object.values(data_name);
console.log(name_list);

let message = localStorage.getItem("transfer");
components_list = message.split(",");
console.log(components_list);

let index_list = [];
for (let i = 0; i < components_list.length; i++) {
  for (let j = 0; j < name_list.length; j++) {
    if (components_list[i] === name_list[j]) {
      index_list.push(j);
    }
  }
}

console.log(index_list);

document.getElementById("cpu").innerText = components_list[0];
document.getElementById("gpu").innerText = components_list[1];
document.getElementById("motherboard").innerText = components_list[2];
document.getElementById("pc_case").innerText = components_list[3];
document.getElementById("power_supply").innerText = components_list[4];
document.getElementById("ram").innerText = components_list[5];
document.getElementById("ssd").innerText = components_list[6];
document.getElementById("hdd").innerText = components_list[7];

document.getElementById("cpu-price").innerText = price_list[index_list[0]];
document.getElementById("gpu-price").innerText = price_list[index_list[1]];
document.getElementById("motherboard-price").innerText =
  price_list[index_list[2]];
document.getElementById("pc_case-price").innerText = price_list[index_list[3]];
document.getElementById("power_supply-price").innerText =
  price_list[index_list[4]];
document.getElementById("ram-price").innerText = price_list[index_list[5]];
document.getElementById("ssd-price").innerText = price_list[index_list[6]];
document.getElementById("hdd-price").innerText = price_list[index_list[7]];

let total_price = 0;
for (let i = 0; i < index_list.length; i++) {
  total_price = total_price + price_list[index_list[i]];
}
console.log(total_price);
document.getElementById("total-price").innerText = total_price;
document.getElementById("price").value = total_price;
