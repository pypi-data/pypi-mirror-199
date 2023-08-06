# DjangoCMS Mapy.cz Markers


The *DjangoCMS Mapy.cz Markers* module is a plugin for the [DjangoCMS](https://www.django-cms.org/) framework.
It is used for displaying map with markers. Map is provided by [Mapy.cz](https://mapy.cz).
Plugin was created on [Mapy API version 4.13 – Neil Armstrong](https://api.mapy.cz/).

## Usage

### Plugin "Mapy.cz Markers"

The **Mapy.cz Markers** plugin displays a map of the Czechia. You can set the map size, location and zoom size. It is also possible to disable map controls (scroll bar and map base types) and mouse wheel zooming. By default, markers that are close to each other are automatically grouped together. This feature can also be turned off.

![Plugin Mapy.cz](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/raw/main/screenshots/plugin-mapycz.png)

![Plugin with cluster](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/raw/main/screenshots/map-with-cluster.png)

### Plugin "Markers"

The **Marker** plugin displays a marker on the map. Each marker includes the address of a point on the map and its exact location, given by latitude and longitude. When entering an address, a whisperer with a list of known addresses is displayed. When you select a marker from the list, its latitude and longitude are automatically added to the marker.

It is also possible to set the title of the tag, which is displayed as the *title* attribute of the icon. You can set the color of the icon or overlay it on your own.

It is possible to enter a business card in the tag. The content of a business card consists of a header, body and footer.

![Plugin Marker on Mapy.cz](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/raw/main/screenshots/choose-marker-address.png)

### Panorama

If the *Styl* plugin with the `mapycz-panorama` class is inserted into the page, the *Panorama* link is displayed in the footer of the business card. Clicking on it will display a panorama of that point in the *Style* plugin (if available in the map).

![Map with panorama](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/raw/main/screenshots/map-with-panorama.png)

### Plugin "Connect address with the map"

The **Connect address with the map** plugin can be used for two purposes.

The first purpose is a whisperer. In the *Address* field, enter the name of the text field for which the whisperer will display a list of known addresses. As the user starts typing an address, a list of addresses matching the one typed will be displayed. Clicking into the list causes the address to be inserted into the address field.

The second purpose is to connect to the map. It is used to set the geographic coordinates of the selected address to be inserted into the appropriate fields of the form. It is also possible to define which fields of the form represent the content of the business card.

Catuion! The plugin must be placed under the **Form** plugin. It uses text fields only of its *superior* form.

![Form with address whisperer](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/raw/main/screenshots/address-whisperer.png)

![Connect address with the map](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/raw/main/screenshots/connect-address-with-map.png)


### Command "Add Mark into Mapy.cz"

With this connection to the map, saved user responses can then be inserted into the map as markers. The web editor selects user responses in the *Form submissions* list and sets the *Add Mark into Mapy.cz* action in the action list. Clicking the *Go* button will create markers on the map from the user submissions.

![Command](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/raw/main/screenshots/run-action-markers-into-map.png)

### Funkction form_submission_field

The `form_submission_field` function allows the list of submitted forms to display links to pages where the Marker specified in the submission data appears in the map.

## Installation

See more in [INSTALL.md](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/blob/main/INSTALL.md).

## Example

How to run the example. For more see [example/HOWTO.md](https://gitlab.nic.cz/djangocms-apps/djangocms-mapycz-markers/-/blob/main/example/HOWTO.md).


## Author

Zdeněk Böhm zdenek.bohm@nic.cz
CZ.NIC, z. s. p. o.

## License

[GPLv3+](https://www.gnu.org/licenses/gpl-3.0.html)
