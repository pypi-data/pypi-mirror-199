pub mod logfermi;

use numpy::{IntoPyArray, PyArray2, PyReadonlyArray2};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

#[pymodule]
fn ase_extension(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn log_fermi<'py>(
        _py: Python<'py>,
        positions: PyReadonlyArray2<f64>,
        radius: f64,
        temperature: f64,
        beta: f64,
    ) -> (f64, &'py PyArray2<f64>) {
        let positions = positions.as_array();
        let (e, e_grad) = logfermi::log_fermi(&positions, radius, temperature, beta);
        (e, e_grad.into_pyarray(_py))
    }

    Ok(())
}
