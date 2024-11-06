import Light from "../components/Light";
import AppBarComponent from '../components/AppBarComponent.jsx';
import LightHandleBar from "../components/LightHandleBar.jsx";

export default function MotionPage() {
    return (
        <div>
            <AppBarComponent />
            <Light />

            <LightHandleBar />
            

        </div>
    );
}