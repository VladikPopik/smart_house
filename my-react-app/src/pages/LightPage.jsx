import Light from '../components/Light';
import AppBarComponent from '../components/AppBarComponent.jsx';
import LightCharts from '../components/LightLayoutGraph.jsx';


export default function MonitoringPage() {
    return (
        <body>
            <AppBarComponent/>
            <Light />
            <LightCharts />
        </body>
    );
}