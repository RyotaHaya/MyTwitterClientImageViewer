<template>
  <a v-bind:href="profile.twitterUrl">
    <v-avatar class="hidden-sm-and-down,mt-n12 mx-auto" color="white" size="36">
      <img
        v-bind:src="profile.iconUrl"
        alt="avatarImage"
        class="avatar-image" /></v-avatar
  ></a>
</template>

<script>
export default {
  data() {
    return {
      profile: {
        twitterUrl: 'https://twitter.com',
        iconUrl:
          'https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light',
        defalutIcon: '~/assets/twitter-logo-icon',
      },
    }
  },
}
</script>
