/**
 * xel_langs {hashmap} maps abbreviations to the actual names of the languages
 */
var xel_langs = {
    "eng": "English",
	"cmn": "Mandarin",
	"spa": "Spanish",
	"fre": "French",
	"ger": "German",
	"jpn": "Japanese"
}

/**
 * xel_examples {hashmap} maps each language to 1-5 exmaples
 */

var xel_examples = {
    "eng": [
		"St. Michael's Church is on 5th st. near the light.",
		"Hello world. My name is Mr. Smith. I work for the U.S. Government and I live in the U.S. I live in New York.",
		"Mr.O'Neill thinks that the boys' stories about Chile's capital aren't amusing.",
		"You can find it at N°. 1026.253.553. That is where the treasure is.",
		"I wasn’t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didn’t mean it.",
		"One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds. . . . The practice was not abandoned. . . .",
		"The Indo-European Caucus won the all-male election 58-32."
	],
	"cmn": [
		"巴拉克·奥巴马在夏威夷出生。他喜欢寿司。",
		"黄山位于安徽省南部黄山市境内，有72峰，主峰莲花峰海拔1864米，与光明顶、天都峰并称三大黄山主峰，为36大峰之一。黄山是安徽旅游的标志。",
		"这里有结婚的和尚未结婚的人。",
		"真的是这样吗... 怎么这么多事儿！"
	],
	"spa": [
		"Mohandas Karamchand Gandhi (Porbandar, India británica; 2 de octubre de 1869–Nueva Delhi, Unión de la India; 30 de enero de 1948) fue el dirigente más destacado del Movimiento de independencia de la India contra el Raj británico, para lo que practicó la desobediencia civil no violenta, además de pacifista, político, pensador y abogado hinduista indio.",
        "Sigmund Freud fue un neurólogo austriaco y fundador del psicoanálisis, un método clínico para tratar la psicopatología a través del diálogo entre un paciente y un psicoanalista. Freud nació de padres judíos gallegos en la ciudad morava de Freiberg, en el Imperio austríaco. Se graduó como doctor en medicina en 1881 en la Universidad de Viena. Freud vivió y trabajó en Viena, donde estableció su práctica clínica en 1886. En 1938, Freud dejó Austria para escapar de la persecución nazi. Murió exiliado en el Reino Unido en 1939.",
		"Barack Hussein Obama II es un político y abogado estadounidense que se desempeñó como el 44º presidente de los Estados Unidos de 2009 a 2017. Miembro del Partido Demócrata, Obama fue el primer presidente afroamericano de los Estados Unidos. Anteriormente se desempeñó como senador de Estados Unidos por Illinois de 2005 a 2008 y como senador del estado de Illinois de 1997 a 2004. ",
		"Mohandas Karamchand Gandhi fue un abogado indio, nacionalista anticolonial y especialista en ética política, que empleó la resistencia no violenta para liderar la exitosa campaña por la independencia de la India del dominio británico y, a su vez, inspiró movimientos por los derechos civiles y la libertad en todo el mundo. El Mahātmā honorífico, que se le aplicó por primera vez en 1914 en Sudáfrica, ahora se usa en todo el mundo."
	], 
	"fre": [
		"Apple cherche à acheter une start-up anglaise pour 1 milliard de dollars."
	],
	"ger": [
		"Die ganze Stadt ist ein Startup: Shenzhen ist das Silicon Valley für Hardw",
		"Sigmund Freud war ein österreichischer Neurologe und der Begründer der Psychoanalyse, einer klinischen Methode zur Behandlung der Psychopathologie im Dialog zwischen einem Patienten und einem Psychoanalytiker. Freud wurde als Sohn galizischer jüdischer Eltern im mährischen Freiberg im österreichischen Reich geboren. Er qualifizierte sich 1881 als Doktor der Medizin an der Universität Wien. Freud lebte und arbeitete in Wien, nachdem er dort 1886 seine klinische Praxis eingerichtet hatte. 1938 verließ Freud Österreich, um der nationalsozialistischen Verfolgung zu entgehen. Er starb 1939 im britischen Exil."
	],
	"jpn": [
		"アップルがイギリスの新興企業を１０億ドルで購入を検討"
	]
}

function clearResults(){
	$("#result-stanza").html( "" );
	$("#result-spacy").html( "" );
	$("#result-udpipe").html( "" );
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
	clearResults();
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
			opt.innerHTML = xel_langs[key];
			selectField.appendChild(opt);
		}
	}	
	selectField.value = "eng";
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
	clearResults();
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
async function postData(url, data_json={}, pfunction, lang, model) {
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
		.then(json_output => {pfunction(json_output, lang, model)}
	);
}

/**
 * @abstract generate the output in the HTML document
 * @yield {NULL}
 */
function outputXEL(json, lang, model) {
	result = document.getElementById("result-" + model)
	json_string = JSON.stringify(json)
	console.log(json_string)
	result.innerHTML +=	json_string.substring(1, json_string.length - 1).replaceAll('\\"', '"')
}

/**
 * @abstract send the post request with data, please modify if your service requires other variables 
 * @yield {NULL}
 */
function runAnnotation() {
	fLang = document.getElementById("lang").value;
	valid_languages = ['eng', 'cmn', 'spa', 'jpn', 'fre', 'ger']
	url_tokenize = "./process"

    if (!valid_languages.includes(fLang)) {
        alert('Sorry! Invalid language...');
        langSelectField = document.getElementById("lang");
        langSelectField.value = 'eng';
        fillExampleSelectField('eng');
        return;
    }

    fText = document.getElementById("text").value;

	packages = document.getElementsByTagName("input");
	for(var i = 0; i < packages.length; i++) {
		if(packages[i].type == "checkbox") {
			if(packages[i].checked == true) {
				data = { "text" : fText , "lang" : fLang , "package" : packages[i].id };
				postData(url_tokenize, data, outputXEL, fLang, packages[i].id);
			} 
		}  
	}
}

/**
 * @abstract submit the form
 * @yield {boolean} false
 */
function formSubmit() {
	clearResults();
	runAnnotation();
	return false;
}
