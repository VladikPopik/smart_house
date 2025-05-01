import AppBarComponent from '../components/AppBarComponent.jsx';
import SettingsTable from '../components/SettingsTable.jsx';
import FaceRegister from '../components/FaceRegister.jsx';

export default function SettingsPage () {
    return (
        <div>
            <AppBarComponent/>
            <FaceRegister></FaceRegister>
            <SettingsTable></SettingsTable>
        </div>
    )
}