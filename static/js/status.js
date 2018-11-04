async function request_api(site, username, backend_config) {
	return await
	$.ajax({
		dataType: 'json',
		url     : `${backend_config.protocol_backend}://${backend_config.host_backend}:${backend_config.port_backend}/check/${site}/${username}`,
	})
	.then((result) => {
		const res = result;
		if (!res['usable'])
			$("#" + site)[0].innerHTML = 'Website Down';
		else if (!res['possible'])
			$("#" + site)[0].innerHTML = 'Impossible';
		else if (res['status'] == '404' || res['status'] == '301')
		$("#" + site)[0].innerHTML = `Available`;
		// handling facebook edge case, when the
		// username exists but the url is not accessible
		else if (site == 'facebook' && res['profile'] == 'hidden')
			$("#" + site)[0].innerHTML = `Taken`;
		else if (res['avatar'])
			$("#" + site)[0].innerHTML =
			`<a href="${res['url']}" target="_blank"> <img class="avatar" src="${res['avatar']}">`;
		else
			$("#" + site)[0].innerHTML = `<a href="${res['url']}" target="_blank">Taken</a>`;
	})
	.fail(() => {
	   $("#" + site)[0].innerHTML = 'Don\'t know';
	});
}

function main ()  {
	// list of supported websites
	const sites = data.sites.split(" ");
	const logos = JSON.parse(data.logos);
	let username = data.username;

	/* backend config */
	const backend_config = {
		protocol_backend: data.protocol_backend,
		host_backend:  data.host_backend,
		port_backend: data.port_backend
	} 
	
	// create cards dynamically for each of the websites
	sites.forEach(website => {
	  const logoElement = constructLogoElement(website, logos);
	  $(".helper").append(`
		<div class="card">
			<p>
				<div class="tooltip">
					<${logoElement.htmlElement} ${logoElement.htmlAttribute}="${logoElement.attributeValue}">
					</${logoElement.htmlElement}>
					<span class="tooltiptext">${website}</span>
				</div>
				<span id='${website}'>
					<i class="fas fa-circle-notch fa-spin"></i>
				</span>
			</p>
		</div>`)
	});

	// iterate over all the websites and call
	// call request_api each of the wesbite
	sites.forEach(website => {
		request_api(website, username, backend_config);
	});
}

function constructLogoElement (website, logos) {
	// defaults to font awesome icons
	let logoElement = {
		attributeValue: `fab fa-${website}`,
		htmlAttribute: 'class',
		htmlElement: 'i',
	};

	if (logos[website]) {
		// the key defined in the yml. e.g., url, fontawesome
		let ymlKey = Object.keys(logos[website])[0];
		// determines html attribute to be used to display icon. e.g., src, class
		logoElement.htmlAttribute = determineLogoHtmlAttribute(ymlKey);
		// determines html element to be used based off of the attribute. e.g., i, img
		logoElement.htmlElement = determineLogoHtmlElement(logoElement.htmlAttribute);
		// gets the attribute value from the yml file.
		logoElement.attributeValue = logos[website][ymlKey];
	}
	return logoElement;
}

function determineLogoHtmlElement(htmlAttribute) {
	let element;
	if (htmlAttribute === 'src') {
		element = 'img';
	} else if (htmlAttribute === 'class') {
		element = 'i';
	}
	return element;
}

function determineLogoHtmlAttribute(key) {
	let attribute;
	if (key === 'url') {
		attribute = 'src';
	} else if (key === 'fontawesome') {
		attribute = 'class';
	} else {
		console.error("Incorrect logo key in yml.")
	}
	return attribute;
}
