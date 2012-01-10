import QtQuick 1.0
import com.nokia.meego 1.0
import "uiconstants.js" as UI

Page {
    orientationLock: PageOrientation.LockPortrait
    Header{
        text: "List Geocaches"
        id: header
    }

    Column {
        anchors.top: header.bottom
        //anchors.topMargin: 8
        spacing: 0
        width: parent.parent.width

        ListButton {
            text: "...in current map view"

            onClicked: {
                pageGeocacheList.source = "GeocacheListPage.qml";
                showDetailsPage(pageGeocacheList.item);
                pageGeocacheList.item.model = tabMap.geocacheModel;
                pageGeocacheList.item.model.sort(0, gps);
            }
            height: 70
        }

        ListButton {
            text: "...having Fieldnotes"

            onClicked: {
                pageGeocacheList.source = "GeocacheListPage.qml";
                showDetailsPage(pageGeocacheList.item);
                pageGeocacheList.item.model = controller.getGeocachesWithFieldnotes();
                pageGeocacheList.item.model.sort(0, gps);
            }
            height: 70
        }

        ListButton {
            text: "...in Favorites"

            onClicked: {
                pageGeocacheList.source = "GeocacheListPage.qml";
                showDetailsPage(pageGeocacheList.item);
                pageGeocacheList.item.model = controller.getMarkedGeocaches();
                pageGeocacheList.item.model.sort(0, gps);
            }
            height: 70
        }
    }



    Loader {
        id: pageGeocacheList
    }



    Menu {
        id: menu
        visualParent: parent

        MenuLayout {
            //MenuItem { text: currentGeocache.found ? "Mark Not Found" : "Mark Found"; }
            MenuItem { text: "Settings"; onClicked: { showSettings(); } }
        }
    }
}
