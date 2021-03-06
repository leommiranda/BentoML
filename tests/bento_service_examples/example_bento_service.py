import bentoml
from bentoml.adapters import (  # FastaiImageInput,
    DataframeInput,
    ImageInput,
    JsonInput,
    LegacyImageInput,
    LegacyJsonInput,
)
from bentoml.handlers import DataframeHandler  # deprecated
from bentoml.service.artifacts.pickle import PickleArtifact


@bentoml.artifacts([PickleArtifact("model")])
@bentoml.env(infer_pip_packages=True)
class ExampleBentoService(bentoml.BentoService):
    """
    Example BentoService class made for testing purpose
    """

    @bentoml.api(
        input=DataframeInput(), mb_max_latency=1000, mb_max_batch_size=2000, batch=True
    )
    def predict(self, df):
        """An API for testing simple bento model service
        """
        return self.artifacts.model.predict(df)

    @bentoml.api(input=DataframeInput(dtype={"col1": "int"}), batch=True)
    def predict_dataframe(self, df):
        """predict_dataframe expects dataframe as input
        """
        return self.artifacts.model.predict_dataframe(df)

    @bentoml.api(DataframeHandler, dtype={"col1": "int"}, batch=True)  # deprecated
    def predict_dataframe_v1(self, df):
        """predict_dataframe expects dataframe as input
        """
        return self.artifacts.model.predict_dataframe(df)

    @bentoml.api(input=ImageInput(), batch=True)
    def predict_image(self, images):
        return self.artifacts.model.predict_image(images)

    @bentoml.api(
        input=LegacyImageInput(input_names=('original', 'compared')), batch=False
    )
    def predict_legacy_images(self, original, compared):
        return self.artifacts.model.predict_legacy_images(original, compared)

    @bentoml.api(input=JsonInput(), batch=True)
    def predict_json(self, input_data):
        return self.artifacts.model.predict_json(input_data)

    @bentoml.api(input=LegacyJsonInput(), batch=False)
    def predict_legacy_json(self, input_data):
        return self.artifacts.model.predict_legacy_json(input_data)

    # Disabling fastai related tests to fix ci build
    # @bentoml.api(input=FastaiImageInput())
    # def predict_fastai_image(self, input_data):
    #     return self.artifacts.model.predict_image(input_data)
    #
    # @bentoml.api(input=FastaiImageInput(input_names=('original', 'compared')))
    # def predict_fastai_images(self, original, compared):
    #     return all(original.data[0, 0] == compared.data[0, 0])
