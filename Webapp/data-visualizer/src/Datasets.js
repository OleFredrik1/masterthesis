import * as d3 from 'd3-fetch';
import {autoType} from 'd3';

export const studies =  ["Abdollahi2019", "Asakura2020", "Bianchi2011", "Boeri2011", "Chen2019", "Duan2021", "Fehlmann2020", "Halvorsen2016", "Jin2017", "Keller2009", "Keller2014", "Keller2020", "Kryczka2021", "Leidinger2011", "Leidinger2014", "Leidinger2016", "Li2017", "Marzi2016", "Nigita2018", "Patnaik2012", "Patnaik2017", "Qu2017", "Reis2020", "Wozniak2015", "Yao2019", "Zaporozhchenko2018"];

export const formatStudyName = (name) =>{
    let ind = name.indexOf("2");
    return name.slice(0, ind) + " [" + name.slice(ind) + "]";
};

//const studies = ["Abdollahi2019", "Kryczka2021"];
/*
const datasets = {};

studies.forEach(async (study) => {
    datasets[study] = await d3.csv('/Datasets/' + study + '.csv', autoType);
    console.log(datasets[study]);
});

export default datasets;
*/
