# NFTag: Non-Fungible Tag #

![image](https://github.com/user-attachments/assets/6a246cd1-ef94-4033-bff2-14b4aa229712)
*Fig 1: Shows NFTag and NFTag application*

**Introduction**

Non-Fungible Tokens (NFTs) have emerged as a revolutionary tool for representing ownership of digital assets on the blockchain. There's a growing need for a system that seamlessly integrates asset management, personalization, and community engagement.

Imagine a world where your valuables are not only secure but also personalized to reflect your unique style. Where every item you own, from your laptop to your beloved pet, is part of a vibrant, decentralized community dedicated to keeping your belongings safe.

NFTag offers a solution that leverages NFTs, Bluetooth and Internet of Things (IoT) technology to create a secure, engaging, and efficient way to manage valuable items. You can attach the NFTag device to valuables such as laptops, pets, or other belongings. It combines the power of NFTs and Bluetooth to offer a unique blend of functionality and personalization for tracking. They come in two flavours; one with ESP32-C3 Wifi Bluetooth Development Board Module, 1.28 Inch Round LCD Display Screen 240X240 IPS and one without.

Visit our web application here: http://3.145.55.152:8050/

**The Problem**

Traditional asset tracking solutions often suffer from several limitations, including:

* Lack of personalization: Traditional trackers are generic and lack the ability for users to express their individuality.
* Security concerns: Many tracking solutions rely on centralized systems, which can be vulnerable to data breaches and security risks.
* Inefficient loss recovery: Current methods often fail to incentivize the community to assist in recovering lost items.
* Fragmented ecosystems: Managing digital and physical assets separately can be cumbersome and inefficient.

**The Solution: NFTag**

The NFTag device addresses these challenges by offering a comprehensive solution for asset tracking. Here's a closer look at its key features:

* Personalization through NFTs:

![image](https://github.com/user-attachments/assets/15a822b1-5425-499e-8f5f-737bd42bfc9a)
*Fig 2: Shows Personalised NFTag customised from the app once connected via bluetooth*

   * Users can customize their trackers by loading their favorite NFTs onto the round LCD screen via Bluetooth from their smartphone or PC.
   * Non-display option: For those who prefer a more subtle tracker, the NFTag is also available without an LCD screen.
     
* Advanced tracking and security:

  ![image](https://github.com/user-attachments/assets/5192f385-8431-4aed-a5e0-e768bcb13ef7)
  *Fig 3: describes tracking of assets using NFTags*

    * Enhanced security with blockchain technology: By leveraging blockchain technology, the NFTag ensures improved security and privacy for users. The decentralized nature of the blockchain provides a secure platform for managing asset information.
    * Bluetooth tracking and alerts: The NFTag utilizes Bluetooth and GPRS location technology to maintain a secure connection with the owner's smartphone, pinpointing the relative location. If the tag becomes separated, an alarm and personalized message can be activated through the web app, broadcasting ownership details to nearby users (within a 20-50 meter range) to aid in recovery.
      
* Community engagement and rewarding:

![image](https://github.com/user-attachments/assets/3448537b-6684-4981-a44f-420196549776)
*Fig 4: Illustrates earning mechanism when users help find lost assets*

  * Decentralized Physical Infrastructure Networks (DePIN): Each NFTag functions as a node within DePIN, contributing to a decentralized network that enhances both security and tracking capabilities. This fosters community engagement and collaborative asset recovery.
  * Token rewards for network participation: Users can earn tokens by actively participating in the network. When they help locate lost items or maintain active devices, they receive $NFTag tokens, creating a "find-to-earn" incentive system that encourages community involvement.

* Integration with Web3 and Blockchain

   * Web3 Wallet Integration: Users can connect their Web3 wallet to the web app. This integration supports NFT customization and secure transaction handling.
   * Earning Mechanism: A "Mining" $NFTag button simulates earning tokens. This feature demonstrates the concept of tokens increasing by the second, providing a preview of the full functionality.


# Demo NFTag Web Application #

**Introduction to the webapp**

images/dash1.PNG
![Fig 6: ](dash1.png)](images/dahsh1.PNG)         |


The NFTg application is a cutting-edge platform that brings the physical and digital worlds together in anetwork through innovative use of NFT technology combined wih bluetooth and Decentralised web3 blockchain application. This web application integrates web3 Ethereum blockchain, allowing users to interact with their NFTags through linking ther wallets, with infura and smart contracts. With NFTags having Bluetooth, users can customize them with their favorite NFT profile pictures (PFPs) and custom messages, and even mine $NFTag tokens while using the platform.


**Platform Overview**
This repository contains the codebase for the NFTag web application, designed and developed as a Minimum Viable Product (MVP). The platform is hosted on an AWS EC2 instance and is accessible at http://3.145.55.152:8050/. Upcoming verions will have sign up an login interfaces to get users up and running smoothly with a click of a button. The platform is simple to use once bluetooth and location features are enabled on the phone. Furthermore, it is mobile responsive with simplicity at its core.

**Key Features**
1. Bluetooth & Location Integration:
The app enables users to turn on/off Bluetooth and location services to interact with nearby NFTags. It is this feature that scans nearby NFTags, connect, enables customization and precisely obtains location of the devices for tracking. They are listed on the dashboard for manual selection, connection and customization.

**Scan & Connect**
The platform scans for nearby NFTags and lists them, allowing users to connect manually. Users can connect/link the devices, disconnect, trigger a lost alert alerm/custom message that will enable easy tracking and tracing.

**NFT PFP Customization**
Once connected, users can upload their favorite NFT PFP thrugh a tailor made feature section, set a custom message, and even add an alert alarm/message settings to the tag. In addition NFTag device names can be changed and customised to suit the user preference. It is through this feature that users help track lost NFTags and earn at the same time helping owners trace their assets. Further, users can change/customise NFT PFPs displayed on their NFTag screens.

**Real-Time Tracking**
NFTags are visualized on a map, making it easy to track their location. Also, to accurately identify them, wheh a user clicks on the marker/icon, hover information is visualised showin gthe nade of the NFTag, owner, its value among other information. The visualization works for the devices that are active/connected to the platform. Any NFTag device that is not connected is not visualised.

**Web3 Wallet Integration**
Leveraging web3 python library, Users are able to be connected to the web3 blockchain infrustructure such as Eutherium. Users can link their web3 wallet by adding their wallet addresses; such as MetaMask, and demonstrate how to customize NFT metadata on the blockchain using smart contracts with the help of Infura and Eutherium network testnets such as Rinkeby and sepolia. Users can access deployed contracts and potentially modify NFT metadata for their own use in the blockchain for NFTags.

**Seamless Connectivity**
Users can connect, disconnect, and customize their NFTags directly from the platform. They can execute many actionas such as;

Lost Tag Alert:
If an NFTag is lost, users can send an alert from/on the platform to indicate that an NFTag status is lost, triggering an alarm and displaying a message on the tag's screen. Users who find the NFTag can leverage on the displayed message and alarm to update the status of the tag on the platform, helping the owner find their asset.

Community Rewards:
Users who help locate lost NFTags are rewarded with $NFTag tokens. With the decebtralised nature of the system and linked web3 wallet users who help to track the lost NFTs are rewarded making the system engaging, rewarding and active. The $NFTag tokens keeps accumulating and incrementing as a sum together with mining.

$NFTag Token Mining:
A dedicated button on the platform allows users to mine $NFTag tokens with a single press. The more you press on the button the more you mine the tokens.

PFP Visualization & Customization:
Users can visualize their favorite NFT PFP on the platform and customize their name tags and custom messages anytime when connected. This is directly pushed to the NFTags connected on the platform. A user only selects an NFTag they wish to customise and make necessary modifications to their GRATT structure and push changes to take effect both on the platform and the device.

**NFTag Development Journey**
MVP Implementation: The initial NFTag model was designed without an LCD screen. In addition, the one with LCD screen to display NFT PFP is under development in its product cycle.
Pending Enhancements: Development of an NFTag with an LCD screen is in progress, with final assembly pending.
Bluetooth Integration: The NFTag firmwares are capable of connecting to a phone via Bluetooth, allowing customization with NFT PFPs directly from the platform.
Deployment. This is the linking point in the physical network that enables tracking and alerting.
The platform is currently deployed on an AWS EC2 instance, providing easy access for users at http://3.145.55.152:8050/.

Getting Started
To get started with NFTag, clone this repository and add necessary AWS S3, mapbox credentials to set up the platform locally.

bash
Copy code
git clone https://github.com/jaredmaks23/nftags-anftagApp-web3-blockchain.git
cd nftags-anftagApp-web3-blockchain



Contributing
We welcome contributions! Whether you're fixing bugs, adding new features, or improving documentation, your efforts are appreciated. Please check out our Contributing Guide for more details.

License
This project is licensed under the MIT License.


