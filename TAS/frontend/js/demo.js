/**
 * xel_langs {hashmap} maps abbreviations to the actual names of the languages
 */
var xel_langs = {
    "eng": "English",
	"cmn": "Mandarin",
	"spa": "Spanish",
}

/**
 * xel_examples {hashmap} maps each language to 1-5 exmaples
 */

var xel_examples = {
    "eng": [
		"Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology through dialogue between a patient and a psychoanalyst. Freud was born to Galician Jewish parents in the Moravian town of Freiberg, in the Austrian Empire. He qualified as a doctor of medicine in 1881 at the University of Vienna. Freud lived and worked in Vienna, having set up his clinical practice there in 1886. In 1938, Freud left Austria to escape Nazi persecution. He died in exile in the United Kingdom in 1939.",
        "Barack Hussein Obama II is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, Obama was the first African-American president of the United States. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004.",
		"Mohandas Karamchand Gandhi was an Indian lawyer, anti-colonial nationalist, and political ethicist, who employed nonviolent resistance to lead the successful campaign for India's independence from British rule, and in turn inspired movements for civil rights and freedom across the world. The honorific Mahātmā, first applied to him in 1914 in South Africa, is now used throughout the world."
	],
	"cmn": [
		"巴拉克·奥巴马在夏威夷出生。他喜欢寿司。",
		"黄山位于安徽省南部黄山市境内，有72峰，主峰莲花峰海拔1864米，与光明顶、天都峰并称三大黄山主峰，为36大峰之一。黄山是安徽旅游的标志。"
		//"西格蒙德·弗洛伊德（Sigmund Freud）是奧地利的神經病學家，也是精神分析的創始人。精神分析是一種通過患者與精神分析人員之間的對話來治療精神病理的臨床方法。 弗洛伊德出生於奧地利帝國摩拉維亞小鎮弗賴貝格的加利西亞猶太父母。 他於1881年在維也納大學獲得醫學博士學位。 弗洛伊德在維也納生活和工作，1886年在維也納開始了臨床工作。1938年，弗洛伊德離開奧地利，逃避了納粹的迫害。 他於1939年在英國流亡。",
		//"巴拉克·侯赛因·奥巴马二世（Barack Hussein Obama II）是一位美国政治家和律师，2009年至2017年担任美国第44任总统。奥巴马是民主党的一员，是美国第一位非裔美国总统。 他曾于2005年至2008年担任伊利诺伊州的美国参议员，并于1997年至2004年担任伊利诺伊州参议员。",
		//"Mohandas Karamchand Gandhi是印度律師，反殖民民族主義者和政治倫理學家，他運用非暴力抵抗力量領導了印度獨立於英國統治之外的成功運動，進而激發了全世界爭取公民權利和自由的運動。 尊敬的Mahātmā於1914年在南非首次應用於他，如今已在全世界使用。",
		// "聽到有關四川地震的消息，我感到震驚，近一萬人喪生。儘管我在那裡沒有親戚，但我是顏，黃的後裔，是中國的同胞。在這個危機時刻，我不禁伸出援手，盡一切可能安慰我的同胞和良心。在餐桌上，我們全家，包括我13歲的女兒和幾乎4歲的兒子，都同意向受災群眾捐款。我女兒決定捐出從父母那裡做家務所得的部分錢。使國家擺脫困境是我們華僑的責任，也是我們華僑的優良傳統。",
		// "1911年革命爆發那年，華僑捐獻了物資，甚至直接參加了革命，流血犧牲，為現代中國革命事業做出了巨大貢獻。當日本人入侵我們時，陳嘉庚大喊，東南亞的中國人幾乎傾注了自己的錢，捐款超過2000萬元，加上華人向在中國的親戚匯款，總金額達數億美元。 （見譚家記的《南橋回憶錄》），是當時國民政府最重要的外彙來源。即使在改革開放後的1980年代初期，中國政府的吸引外資政策也得以實現。實際上並沒有吸引太多西方投資，在那個時期外國投資的主要來源仍然是海外華人投資。"
	],
	"spa": [
        "Sigmund Freud fue un neurólogo austriaco y fundador del psicoanálisis, un método clínico para tratar la psicopatología a través del diálogo entre un paciente y un psicoanalista. Freud nació de padres judíos gallegos en la ciudad morava de Freiberg, en el Imperio austríaco. Se graduó como doctor en medicina en 1881 en la Universidad de Viena. Freud vivió y trabajó en Viena, donde estableció su práctica clínica en 1886. En 1938, Freud dejó Austria para escapar de la persecución nazi. Murió exiliado en el Reino Unido en 1939.",
		"Barack Hussein Obama II es un político y abogado estadounidense que se desempeñó como el 44º presidente de los Estados Unidos de 2009 a 2017. Miembro del Partido Demócrata, Obama fue el primer presidente afroamericano de los Estados Unidos. Anteriormente se desempeñó como senador de Estados Unidos por Illinois de 2005 a 2008 y como senador del estado de Illinois de 1997 a 2004. ",
		"Mohandas Karamchand Gandhi fue un abogado indio, nacionalista anticolonial y especialista en ética política, que empleó la resistencia no violenta para liderar la exitosa campaña por la independencia de la India del dominio británico y, a su vez, inspiró movimientos por los derechos civiles y la libertad en todo el mundo. El Mahātmā honorífico, que se le aplicó por primera vez en 1914 en Sudáfrica, ahora se usa en todo el mundo."
	], 
}

/**
 * @abstract change the example options based on the updated language options
 * @param {string} lang a kind of langage in string
 * @yield {NULL}
 */
function fillExampleSelectField(lang) {
	$("#example").empty();
	selectField = document.getElementById("example");
	textField = document.getElementById("text");
	idx = 0;
	for (var example in xel_examples[lang]) {
		var opt = document.createElement("option");
		opt.value=idx;
		opt.innerHTML = xel_examples[lang][idx].substring(0,50)+"..."; 
		selectField.appendChild(opt);
		idx += 1;
	}	
	selectField.value = "0";
	textField.value = xel_examples[lang][0];
	$("#result").html( "" );
}

/**
 * @abstract load the language options in the field
 * @yield {NULL}
 */
function fillLanguageSelectField() {
	selectField = document.getElementById("lang");
	textField = document.getElementById("text");
	for (var key in xel_langs) {
		if (xel_langs.hasOwnProperty(key)) {           
			var opt = document.createElement("option");
			opt.value=key;
			opt.innerHTML = xel_langs[key]; // ["lang"]; 
			selectField.appendChild(opt);
		}
	}	
	selectField.value = "eng";
	// textField.value = xel_langs["eng"]["text"];
	fillExampleSelectField(selectField.value)
}

/**
 * @abstract fill in the text field given a lang and a example chosen
 * @yield {NULL}
 */
function newExampleSelect() {
	langSelectField = document.getElementById("lang");
	lang = langSelectField.value;
	exampleSelectField = document.getElementById("example");
	example = exampleSelectField.value;
	textField = document.getElementById("text");
	textField.value = xel_examples[lang][example]; 
	$("#result").html( "" );
}

/**
 * @abstract update the examples when a new language is chosen
 * @yield {NULL}
 */
function newLanguageSelect() {
	langSelectField = document.getElementById("lang");
    lang = langSelectField.value;
	fillExampleSelectField(lang);
}

/**
 * @abstract helper function to deliver the post request
 * @yield {NULL}
 */
async function postData(url='http://dickens.seas.upenn.edu:4049/anns', data_json={}, pfunction) {
    console.log("input: " + JSON.stringify(data_json))
    fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Accept': "application/json, text/plain, */*",
            'Content-Type': "application/json;charset=utf-8"
        },
        //mode: 'no-cors',
        body: JSON.stringify(data_json)
	}).then(resp => resp.json())
		.then(json_output => {pfunction(json_output)}
	);
}

/**
 * @abstract generate the output in the HTML document
 * @yield {NULL}
 */
function outputXEL(json) {
	console.log("XEL resulting json: " + JSON.stringify(json));
	result = document.getElementById("result")
	result.innerHTML += JSON.stringify(json, null, 2) + '<br><br>'
}

/**
 * @abstract send the post request with data, please modify if your service requires other variables 
 * @yield {NULL}
 */
function runAnnotation() {
	fLang = document.getElementById("lang").value;
	valid_languages = ['eng', 'cmn', 'spa']
    if (!valid_languages.includes(fLang)) {
        alert('Sorry! Only English, Chinese, and Spanish are supported now.');
        langSelectField = document.getElementById("lang");
        langSelectField.value = 'eng';
        fillExampleSelectField('eng');
        return;
    }

    fText = document.getElementById("text").value;
    data = '{ "text" : "' + fText +  '" ,' + '"lang" : "' + fLang + '" }';
	
	// we can post data to multiple service
    // url="http://dickens.seas.upenn.edu:4049/anns";
	url_tokenize = "http://localhost:8081/process"
	postData(url_tokenize, JSON.parse(data), outputXEL);
}

/**
 * @abstract submit the form
 * @yield {boolean} false
 */
function formSubmit() {
	$("#result").html( "" );
	runAnnotation();
	return false;
}
