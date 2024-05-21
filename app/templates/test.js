const ps = require("prompt-sync");
const prompt = ps();

let s = prompt();
switch(s){
    case "Тар-тар из говядины с битыми огурцами":
        console.log("Заказ добавлен");
        break;
    case "Мясные деликатесы":
        console.log("Заказ добавлен");
        break;
    case "Цезарь с цыпленком":
        console.log("Заказ добавлен");
        break;
    case "Спагетти Карбонара":
        console.log("Заказ добавлен");
        break;
    case "Сырная тарелка":
        console.log("Заказ добавлен");
        break;
    default:
        console.log("Нет такого блюда в меню");
}