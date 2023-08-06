function setValueOrContent(node, value) {
    if (node) {
        if (node.nodeName === 'SELECT') {
            const option = document.createElement('option')
            option.value = value
            option.innerHTML = value
            node.appendChild(option)
            node.value = value
        } else {
            if (node.value === undefined) {
                node.textContent = value
            } else {
                node.value = value
            }
        }
    }
}


function addressSuggest() {
    for(const node of document.getElementsByTagName("mapycz-suggest-address")) {
        const address = document.querySelector(`input[name=${node.dataset.address}]`)
        if (!address || address.value === undefined) {
            console.error(`Element Address does not have attribute "value". Selector: input[name=${node.dataset.address}]`)
            return
        }
        const suggest = new SMap.Suggest(address)
        // Restriction for the Czechia.
        suggest.urlParams({bounds: "48.5370786,12.0921668|51.0746358,18.8927040"})
        suggest.addListener("suggest", function(suggestData) {
            const message = [suggestData.data.title]
            if (suggestData.data.secondRow) {
                message.push(suggestData.data.secondRow)
            }
            if (suggestData.data.thirdRow) {
                message.push(suggestData.data.thirdRow)
            }
            address.value = message.join('; ')
            if (node.dataset.latitude && suggestData.data.latitude) {
                setValueOrContent(document.querySelector(`input[name=${node.dataset.latitude}]`), suggestData.data.latitude)
            }
            if (node.dataset.longitude && suggestData.data.longitude) {
                setValueOrContent(document.querySelector(`input[name=${node.dataset.longitude}]`), suggestData.data.longitude)
            }
        })
    }
}

function initAddressSuggest() {
    Loader.load(null, {suggest: true}, addressSuggest)
}

window.addEventListener("load", initAddressSuggest)
