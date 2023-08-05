import tensorflow as tf

from calotron.models.Discriminator import Discriminator


class PairwiseDiscriminator(Discriminator):
    def __init__(
        self,
        output_units,
        output_activation=None,
        latent_dim=64,
        deepsets_num_layers=5,
        deepsets_hidden_units=128,
        dropout_rate=0.1,
        name=None,
        dtype=None,
    ) -> None:
        super().__init__(
            output_units=output_units,
            output_activation=output_activation,
            latent_dim=latent_dim,
            deepsets_num_layers=deepsets_num_layers,
            deepsets_hidden_units=deepsets_hidden_units,
            dropout_rate=dropout_rate,
            name=name,
            dtype=dtype,
        )

        # Single-target classifier
        # self._seq = self._seq[:-1]

    def call(self, x) -> tf.Tensor:
        batch_size = tf.shape(x)[0]
        length = tf.shape(x)[1]
        depth = tf.shape(x)[2]

        # Pairwise arrangement
        x_1 = tf.tile(x[:, :, None, :], (1, 1, tf.shape(x)[1], 1))
        x_2 = tf.tile(x[:, None, :, :], (1, tf.shape(x)[1], 1, 1))
        output = tf.concat([x_1, x_2], axis=-1)
        output = tf.reshape(output, (batch_size, length**2, 2 * depth))
        output = self._deep_sets(output)
        for layer in self._seq:
            output = layer(output)

        # Single-target classification
        # x = self._deep_sets(x)
        # for layer in self._seq:
        #    x = layer(x)

        return output
