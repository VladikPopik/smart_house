import Light from "../components/Light";
import AppBarComponent from '../components/AppBarComponent.jsx';
import LightHandleBar from "../components/LightHandleBar.jsx";

export default function MotionPage() {
    return (
        <div>
            <AppBarComponent />
            {/* <iframe src='${config.protocol}://127.0.0.1:8000/light' className='full_screen'></iframe> */}
            <Light />

            <LightHandleBar />
            

        </div>
    );
}