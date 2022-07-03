export const getRandomColorList = (lengthList) => {
  console.log(lengthList);
  let listColor = [];
  for (let _index of Array(lengthList).keys()) {
    const randomNum = () => Math.floor(Math.random() * (235 - 52 + 1) + 52);
    const randomRGB = () => `rgb(${randomNum()}, ${randomNum()}, ${randomNum()}, 0.35)`;

    console.log(randomRGB);

    listColor.push(randomRGB());
  }

  console.log(listColor);

  return listColor;
};
