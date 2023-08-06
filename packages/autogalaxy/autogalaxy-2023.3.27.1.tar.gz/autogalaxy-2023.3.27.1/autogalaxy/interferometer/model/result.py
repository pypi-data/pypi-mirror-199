import autoarray as aa

from autogalaxy.analysis.result import ResultDataset
from autogalaxy.galaxy.galaxy import Galaxy
from autogalaxy.plane.plane import Plane
from autogalaxy.interferometer.fit_interferometer import FitInterferometer


class ResultInterferometer(ResultDataset):
    """
    After the non-linear search of a fit to an interferometer dataset is complete it creates
    this `ResultInterferometer` object, which includes:

    - The samples of the non-linear search (E.g. MCMC chains, nested sampling samples) which are used to compute
    the maximum likelihood model, posteriors and other properties.

    - The model used to fit the data, which uses the samples to create specific instances of the model (e.g.
    an instance of the maximum log likelihood model).

    - The non-linear search used to perform the model fit.

    This class contains a number of methods which use the above objects to create the max log likelihood `Plane`,
    `FitInterferometer`, hyper-galaxy images,etc.

    Parameters
    ----------
    samples
        A PyAutoFit object which contains the samples of the non-linear search, for example the chains of an MCMC
        run of samples of the nested sampler.
    model
        The PyAutoFit model object, which includes model components representing the galaxies that are fitted to
        the interferometer data.
    search
        The non-linear search used to perform this model-fit.

    Returns
    -------
    ResultInterferometer
        The result of fitting the model to the interferometer dataset, via a non-linear search.
    """

    @property
    def max_log_likelihood_fit(self) -> FitInterferometer:
        """
        An instance of a `FitInterferometer` corresponding to the maximum log likelihood model inferred by the
        non-linear search.
        """
        hyper_background_noise = self.analysis.hyper_background_noise_via_instance_from(
            instance=self.instance_copy
        )

        instance = self.analysis.instance_with_associated_hyper_images_from(
            instance=self.instance_copy
        )

        plane = self.analysis.plane_via_instance_from(instance=instance)

        return self.analysis.fit_interferometer_via_plane_from(
            plane=plane, hyper_background_noise=hyper_background_noise
        )

    @property
    def max_log_likelihood_plane(self) -> Plane:
        """
        An instance of a `Plane` corresponding to the maximum log likelihood model inferred by the non-linear search.

        The `Plane` is computed from the `max_log_likelihood_fit`, as this ensures that all linear light profiles
        are converted to normal light profiles with their `intensity` values updated.
        """
        return (
            self.max_log_likelihood_fit.model_obj_linear_light_profiles_to_light_profiles
        )

    @property
    def real_space_mask(self) -> aa.Mask2D:
        """
        The real space mask used by this model-fit.
        """
        return self.max_log_likelihood_fit.interferometer.real_space_mask

    def visibilities_for_galaxy(self, galaxy: Galaxy) -> aa.Visibilities:
        """
        Given an instance of a `Galaxy` object, return an image of the galaxy via the the maximum log likelihood fit.

        This image is extracted via the fit's `galaxy_model_image_dict`, which is necessary to make it straight
        forward to use the image as hyper-images.

        Parameters
        ----------
        galaxy
            A galaxy used by the model-fit.

        Returns
        -------
        ndarray or None
            A numpy arrays giving the model image of that galaxy.
        """
        return self.max_log_likelihood_fit.galaxy_model_visibilities_dict[galaxy]

    @property
    def visibilities_galaxy_dict(self) -> {str: Galaxy}:
        """
        A dictionary associating galaxy names with model visibilities of those galaxies.
        """
        return {
            galaxy_path: self.visibilities_for_galaxy(galaxy)
            for galaxy_path, galaxy in self.path_galaxy_tuples
        }

    @property
    def hyper_galaxy_visibilities_path_dict(self):
        """
        A dictionary associating 1D hyper_galaxies galaxy visibilities with their names.

        This is used for creating the hyper-dataset used by Analysis objects to adapt aspects of a model to the dataset
        being fitted.
        """

        hyper_galaxy_visibilities_path_dict = {}

        for path, galaxy in self.path_galaxy_tuples:
            hyper_galaxy_visibilities_path_dict[path] = self.visibilities_galaxy_dict[
                path
            ]

        return hyper_galaxy_visibilities_path_dict

    @property
    def hyper_model_visibilities(self) -> aa.Visibilities:
        """
        The hyper model visibilities used by AnalysisInterferometer objects to adapt aspects of a model to the dataset
        being fitted.

        The hyper model visibilities are the sum of the hyper galaxy visibilities of every individual galaxy.
        """
        hyper_model_visibilities = aa.Visibilities.zeros(
            shape_slim=(self.max_log_likelihood_fit.visibilities.shape_slim,)
        )

        for path, galaxy in self.path_galaxy_tuples:
            hyper_model_visibilities += self.hyper_galaxy_visibilities_path_dict[path]

        return hyper_model_visibilities
