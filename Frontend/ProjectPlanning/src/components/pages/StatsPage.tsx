import { useState, useEffect } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { apiService } from '../../services/api';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend);

export function StatsPage() {
  const [statsData, setStatsData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await apiService.obtainStats();
        setStatsData(data);
      } catch (err) {
        setError('Lo lamentamos, no hemos podido cargar este contenido, por favor intentelo más tarde.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <div className="p-6 text-center">Cargando...</div>;
  }

  if (error) {
    return <div className="p-6 text-center text-red-600">{error}</div>;
  }

  if (!statsData) {
    return <div className="p-6 text-center">No data available</div>;
  }

  // Chart data for each statistic
  const enTerminoChartData = {
    labels: ['En Término', 'Resto'],
    datasets: [
      {
        data: [
          statsData.casosExitososEnTermino?.promedio_porcentaje || 0,
          100 - (statsData.casosExitososEnTermino?.promedio_porcentaje || 0)
        ],
        backgroundColor: ['#10B981', '#E5E7EB'],
        borderWidth: 2,
        borderColor: '#fff',
        hoverOffset: 4
      }
    ]
  };

  const fueraPlazoChartData = {
    labels: ['Fuera de Plazo', 'Resto'],
    datasets: [
      {
        data: [
          statsData.casosFueraDePlazo?.promedio_porcentaje || 0,
          100 - (statsData.casosFueraDePlazo?.promedio_porcentaje || 0)
        ],
        backgroundColor: ['#EF4444', '#E5E7EB'],
        borderWidth: 2,
        borderColor: '#fff',
        hoverOffset: 4
      }
    ]
  };

  const sinColaboracionChartData = {
    labels: ['Sin Colaboración', 'Resto'],
    datasets: [
      {
        data: [
          statsData.casosSinColaboracion?.promedio_porcentaje || 0,
          100 - (statsData.casosSinColaboracion?.promedio_porcentaje || 0)
        ],
        backgroundColor: ['#3B82F6', '#E5E7EB'],
        borderWidth: 2,
        borderColor: '#fff',
        hoverOffset: 4
      }
    ]
  };

  const chartOptions = {
    cutout: '60%',
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          boxWidth: 12,
          font: {
            size: 11
          }
        }
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            return `${context.label}: ${context.parsed}%`;
          }
        }
      }
    },
    maintainAspectRatio: false
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-6">Estadísticas de los proyecto</h2>
      
      {/* Cards Display */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <h3 className="font-semibold text-green-800 mb-2">En Término</h3>
          <p className="text-2xl font-bold text-green-600">
            {statsData.casosExitososEnTermino?.promedio_porcentaje || 0}%
          </p>
          <p className="text-sm text-green-700 mt-1">
            {statsData.casosExitososEnTermino?.casos_en_termino || 0} de {statsData.casosExitososEnTermino?.total_casos || 0} casos
          </p>
        </div>

        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <h3 className="font-semibold text-red-800 mb-2">Fuera de Plazo</h3>
          <p className="text-2xl font-bold text-red-600">
            {statsData.casosFueraDePlazo?.promedio_porcentaje || 0}%
          </p>
          <p className="text-sm text-red-700 mt-1">
            {statsData.casosFueraDePlazo?.casos_fuera_plazo || 0} de {statsData.casosFueraDePlazo?.total_casos || 0} casos
          </p>
        </div>

        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h3 className="font-semibold text-blue-800 mb-2">Sin Colaboración</h3>
          <p className="text-2xl font-bold text-blue-600">
            {statsData.casosSinColaboracion?.promedio_porcentaje || 0}%
          </p>
          <p className="text-sm text-blue-700 mt-1">
            {statsData.casosSinColaboracion?.casos_sin_colaboracion || 0} de {statsData.casosSinColaboracion?.total_casos || 0} casos
          </p>
        </div>
      </div>

      {/* Pie Charts Display */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* En Término Chart */}
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-green-800 text-center mb-3">En Término</h3>
          <div className="h-48">
            <Doughnut data={enTerminoChartData} options={chartOptions} />
          </div>
          <div className="text-center mt-2">
            <p className="text-sm text-gray-600">
              {statsData.casosExitososEnTermino?.casos_en_termino || 0}/{statsData.casosExitososEnTermino?.total_casos || 0} casos
            </p>
          </div>
        </div>

        {/* Fuera de Plazo Chart */}
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-red-800 text-center mb-3">Fuera de Plazo</h3>
          <div className="h-48">
            <Doughnut data={fueraPlazoChartData} options={chartOptions} />
          </div>
          <div className="text-center mt-2">
            <p className="text-sm text-gray-600">
              {statsData.casosFueraDePlazo?.casos_fuera_plazo || 0}/{statsData.casosFueraDePlazo?.total_casos || 0} casos
            </p>
          </div>
        </div>

        {/* Sin Colaboración Chart */}
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-blue-800 text-center mb-3">Sin Colaboración</h3>
          <div className="h-48">
            <Doughnut data={sinColaboracionChartData} options={chartOptions} />
          </div>
          <div className="text-center mt-2">
            <p className="text-sm text-gray-600">
              {statsData.casosSinColaboracion?.casos_sin_colaboracion || 0}/{statsData.casosSinColaboracion?.total_casos || 0} casos
            </p>
          </div>
        </div>
      </div>

      {/* Combined Overview Chart */}
      <div className="mt-8 bg-gray-50 p-6 rounded-lg border">
        <h3 className="font-semibold text-gray-800 text-center mb-4">Distribución General</h3>
        <div className="max-w-md mx-auto h-64">
          <Doughnut 
            data={{
              labels: ['En Término', 'Fuera de Plazo', 'Sin Colaboración'],
              datasets: [
                {
                  data: [
                    statsData.casosExitososEnTermino?.promedio_porcentaje || 0,
                    statsData.casosFueraDePlazo?.promedio_porcentaje || 0,
                    statsData.casosSinColaboracion?.promedio_porcentaje || 0
                  ],
                  backgroundColor: ['#10B981', '#EF4444', '#3B82F6'],
                  borderWidth: 3,
                  borderColor: '#fff',
                  hoverOffset: 8
                }
              ]
            }}
            options={{
              plugins: {
                legend: {
                  position: 'bottom' as const,
                },
                tooltip: {
                  callbacks: {
                    label: function(context: any) {
                      return `${context.label}: ${context.parsed}%`;
                    }
                  }
                }
              },
              maintainAspectRatio: false
            }}
          />
        </div>
      </div>
    </div>
  );
}