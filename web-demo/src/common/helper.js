export const getRandomColorList = (lengthList) => {
  let listColor = [];
  for (let _index of Array(lengthList).keys()) {
    const randomNum = () => Math.floor(Math.random() * (235 - 52 + 1) + 52);
    const randomRGB = () => `rgb(${randomNum()}, ${randomNum()}, ${randomNum()}, 0.35)`;
    listColor.push(randomRGB());
  }
  return listColor;
};

export const parsePrice = (price) => {
  return new Intl.NumberFormat('it-IT', {
    style: 'decimal',
    currency: 'VND',
  }).format(price);
};
