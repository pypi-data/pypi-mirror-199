function createMap(nodeId) {
    const mapId = `mapycz-markers-${nodeId}`
    const node = document.getElementById(mapId)
    const center = SMap.Coords.fromWGS84(node.dataset.map_longitude, node.dataset.map_latitude)
    const map = new SMap(JAK.gel(mapId), center, node.dataset.map_zoom)
    if (node.dataset.controls === 'True') {
        map.addDefaultLayer(SMap.DEF_OPHOTO)
        map.addDefaultLayer(SMap.DEF_TURIST)
        map.addDefaultLayer(SMap.DEF_TURIST_WINTER)
        map.addDefaultLayer(SMap.DEF_HISTORIC)
        map.addDefaultLayer(SMap.DEF_BASE).enable()

        const layerSwitch = new SMap.Control.Layer({
          width: 70,
          items: 5,
          page: 4
        });
        layerSwitch.addDefaultLayer(SMap.DEF_BASE)
        layerSwitch.addDefaultLayer(SMap.DEF_OPHOTO)
        layerSwitch.addDefaultLayer(SMap.DEF_TURIST)
        layerSwitch.addDefaultLayer(SMap.DEF_TURIST_WINTER)
        layerSwitch.addDefaultLayer(SMap.DEF_HISTORIC)
        map.addControl(layerSwitch, {left:"8px", top:"9px"})

        map.addDefaultControls()
    } else {
        map.addDefaultLayer(SMap.DEF_BASE).enable()
    }
    if (node.dataset.no_zoom === 'True') {
        const controls = map.getControls();
        controls.forEach(control => {
            if (control instanceof SMap.Control.Mouse) {
                 control.configure(SMap.MOUSE_PAN | SMap.MOUSE_ZOOM)
            }
        })
    }
    if (!(node.dataset.map_width || node.dataset.map_height)) {
        const sync = new SMap.Control.Sync({bottomSpace:30})
        map.addControl(sync)
    }
    const is_panorama = document.querySelector(".mapycz-panorama-inner")
    // Create Map markers
    const markers = Array.from(document.querySelectorAll(`#${mapId} marker`)).map(
        (marker, index) => createMark(marker, `${mapId}-${index + 1}`, is_panorama)
    )
    if (markers.length) {
        const layer = new SMap.Layer.Marker()
        map.addLayer(layer)
        if (node.dataset.clusterer === "True" && node.dataset.controls === 'True') {
            const clusterer = new SMap.Marker.Clusterer(map)
            layer.setClusterer(clusterer)
        }
        markers.forEach(marker => {
            layer.addMarker(marker)
        })
        layer.enable()
    }
}

function createMark(node, elementId, is_panorama) {
    const card = new SMap.Card()
    if (node.dataset.card_width || node.dataset.card_heigth) {
        card.setSize(node.dataset.card_width, node.dataset.card_heigth)
    }
    let displayCard = false
    if (node.dataset.card_header) {
        card.getHeader().innerHTML = node.dataset.card_header
        displayCard = true
    }
    if (node.dataset.card_body) {
        card.getBody().innerHTML = node.dataset.card_body
        displayCard = true
    }
    if (node.dataset.card_footer) {
        card.getFooter().innerHTML = node.dataset.card_footer
        displayCard = true
    }
    const options = {}
    if (node.dataset.title) {
        options['title'] = node.dataset.title
    }

    if (node.dataset.img_path) {
        const mark = JAK.mel("div")
        const colors = ['red', 'yellow', 'blue']
        const src = colors.includes(node.dataset.img_path) ? SMap.CONFIG.img + `/marker/drop-${node.dataset.img_path}.png` : node.dataset.img_path
        const image = JAK.mel("img", {src: src})
        mark.appendChild(image)
        const img_styles = node.dataset.img_styles ? JSON.parse(node.dataset.img_styles) : {position: "absolute", left: 0, top: "2px", textAlign: "center", width: "22px", color: "white", fontWeight: "bold"}
        const label = JAK.mel("div", {}, img_styles)
        if (node.dataset.img_text) {
            label.innerHTML = node.dataset.img_text
        }
        mark.appendChild(label)
        options.url = mark
    }

    const position = SMap.Coords.fromWGS84(node.dataset.longitude, node.dataset.latitude)
    const marker = new SMap.Marker(position, elementId, options)

    if (displayCard || is_panorama) {
        if (is_panorama) {
            const label = gettext("Panorama")
            const title = gettext("Display Panorama of this place.")
            card.getFooter().innerHTML += ` <a href="javascript:displayPanorama(${node.dataset.longitude}, ${node.dataset.latitude})" title="${title}">${label}</a>`
        }
        marker.decorate(SMap.Marker.Feature.Card, card)
    }
    return marker
}

function displayPanorama(longitude, latitude) {
    document.querySelector(".mapycz-panorama").style.display = "block"
    const nodeScene = document.querySelector(".mapycz-panorama-inner")
    nodeScene.innerHTML = ''
    nodeScene.style.height = "600px"
    const panoramaScene = new SMap.Pano.Scene(nodeScene)
    SMap.Pano.getBest(SMap.Coords.fromWGS84(longitude, latitude)).then(place => {
        panoramaScene.show(place, {yaw: 1.8 * Math.PI})
    }, e => {
        console.error(e)
        const ul = document.createElement('ul')
        ul.classList.add('errormessages')
        const li = document.createElement('li')
        li.classList.add('error')
        li.textContent = gettext('No panorama is available for this location.')
        ul.appendChild(li)
        nodeScene.innerHTML = ''
        nodeScene.style.height = ''
        nodeScene.appendChild(ul)
    })
}

function loadMap(mapId) {
    Loader.async = true
    Loader.lang = document.documentElement.lang
    Loader.load(null, {pano: true}, function () {createMap(mapId)})
}

function initPanorama() {
    const nodeScene = document.querySelector(".mapycz-panorama")
    if (nodeScene) {
        nodeScene.style.display = "none"
        // Inner
        const inner = document.createElement('div')
        inner.classList.add('mapycz-panorama-inner')
        nodeScene.appendChild(inner)
        // Link
        const link = document.createElement('div')
        link.classList.add('close')
        link.textContent = "×"
        nodeScene.appendChild(link)
        link.addEventListener("click", function (event) {
            const nodePanorama = event.target.closest(".mapycz-panorama")
            nodePanorama.style.display = "none"
            const nodeScene = nodePanorama.querySelector(".mapycz-panorama-inner")
            nodeScene.innerHTML = ''
            nodeScene.style.height = "0"
        })
    }
}

pluginMapId = document.currentScript.dataset.mapid

window.addEventListener("load", function () {
    initPanorama()
    loadMap(pluginMapId)
})
